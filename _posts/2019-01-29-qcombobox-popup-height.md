---
layout: single
title:  "Qt: QComboBox 设置下拉菜单高度的几种方法"
date:   2019-01-29
categories:
- Computer Tech
tags: [Qt]
comments: true
---

最近业余写了一些 Qt, 给 [DDE Dock](https://github.com/linuxdeepin/dde-dock) 写了两个插件, 遇到一个 Qt 的设计缺陷. 记录一下解决方案. 

在使用包含很长的可选项的 [QComboBox](http://doc.qt.io/qt-5/qcombobox.html) 时, deepin 下的 stylesheet 定义导致了一个顶天立地的下拉 (弹出) 菜单: 

![初始状态]({{ site.url }}/figure/2019-01/qcombobox/raw.png){:height="30%" width="30%"}

极丑陋. `QComboBox::setMaxVisibleItems` 无效被忽略了. 根据[文档](http://doc.qt.io/qt-5/qcombobox.html#maxVisibleItems-prop)应该是 deepin
的主题样式主要在参考 MacOS 所以设置了 `QStyle::SH_ComboBox_Popup`. 

这个选项主要是使得 QComboBox 的下拉菜单以弹出的方式展示, 与此同时会使得 `MaxVisibleItems` 选项被忽略. 
然而 Qt 没有提供接口限制弹出菜单添加高度 (为此我真是找的很辛苦啊..). 

### 调整 View: 失败 ###

根据 Model/View 的结构, 直接限制 View 的高度, 会使得显示的条目长度受限, 但 Qt 的设计缺陷使得弹出的菜单仍然是原来的长度. 

```
combobox->view()->setMaximumHeight(HEIGHT);
```

效果是这样的: 

![有限长view]({{ site.url }}/figure/2019-01/qcombobox/limitview.png){:height="30%" width="30%"}

这绝壁是 Qt 的设计缺陷啊.. (我是不是应该提一个 issue...)

### `QProxyStyle` 覆盖 ###

前面提到 `MaxVisibleItems` 被忽略是因为设置了 `QStyle::SH_ComboBox_Popup`, 于是这里有了第一个解决方案: 写一个 `QProxyStyle` 来覆盖掉这个设置. 

```
#include <QApplication>
#include <QProxyStyle>
class NonPopupComboBoxStyle : public QProxyStyle
{
  public:
    LimitedHeightCombobox (): QProxyStyle(qApp->style()) {}
    virtual int styleHint(StyleHint hint, const QStyleOption *option = nullptr,
                          const QWidget *widget = nullptr,
                          QStyleHintReturn *returnData = nullptr) const override;
};

int LimitedHeightCombobox::styleHint(StyleHint hint,
                                     const QStyleOption *option,
                                     const QWidget *widget,
                                     QStyleHintReturn *returnData) const {
    switch (hint) {
    case QStyle::SH_ComboBox_Popup:
        return 0; // 0=false
    default:
        return QProxyStyle::styleHint(hint, option, widget, returnData);
    }
}
```

值得注意的是, `QProxyStyle` 在 Qt 文档中的[例子](http://doc.qt.io/qt-5/qproxystyle.html#details)没有构造函数, 
于是就没有继承应用 (`qApp`) 的样式, 而会使用 Qt 的默认的样式. 

有了这个 `NonPopupComboBoxStyle` 之后, 就可以用这样的代码来覆盖样式

```
combobox->setStyle(new NonPopupComboBoxStyle);
```

![nonpopup]({{ site.url }}/figure/2019-01/qcombobox/nonpopup.png)

大多数使用场景应该这样就足够令人满意了. 然而我还希望能够使用弹出式的菜单以适应特别宽的条目, 而不是被 QComboBox 的宽度限制住. 
于是有了下面这种解决方案: 

### 强行改写弹出菜单的尺寸 ###

Qt 没有给接口, 但是 `QObject` 可以通过 `findChild` 定位到这个控件. 于是:

```
combobox->view()->setMaximumHeight(HEIGHT);
combobox->View()->setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
combobox->findChild<QFrame*>()->setMaximumHeight(HEIGHT);
```

特别需要注意的是, `findChild` 找到的组建, 设置高度绝对不能小于 `view` 的高度, 否则会出现 Segment Fault. 
另外, [源代码](https://github.com/qt/qtbase/blob/5733dfbd90fd059e7310786faefb022b00289592/src/widgets/widgets/qcombobox.cpp)第614行在 
`popup` 模式下会禁用 scrollbar, 这个设置也需要覆盖. 

检查 Qt 相关的[源代码](https://github.com/qt/qtbase/blob/5733dfbd90fd059e7310786faefb022b00289592/src/widgets/widgets/qcombobox.cpp)第2648行.
这里找到的 `QFrame` 实际上是个 `QComboBoxPrivateContainer`. 而且似乎可能是在执行 `QComboBoxPrivate::viewContainer()` 时动态生成的. 
所以更理想的用法应该是继承 `QComboBox` 类并重写 `showPopup` 方法, 确保不会因为重新创建 `container` 使得运行出现错误. 

```
class LimitedHightComboBox: public QComboBox {
    Q_OBJECT

public:
    LimitedHightComboBox(int h, QWidget *parent=nullptr);
    virtual void showPopup () override;

private:
    int height;
};

LimitedHightComboBox::LimitedHightComboBox(int h, QWidget *parent):
    QComboBox(parent), height(h) {
    view()->setMaximumHeight(height);
    view()->setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
}

void LimitedHightComboBox::showPopup() {
    QComboBox::showPopup();
    QFrame *popup = findChild<QFrame*>();
    popup->setMaximumHeight(height);
    // Position vertically so the curently selected item lines up
    // with the combo box, inspired by QComboBox source code
    QStyleOptionComboBox opt;
    initStyleOption(&opt);
    QPoint above = mapToGlobal(style()->subControlRect(
                                   QStyle::CC_ComboBox, &opt,
                                   QStyle::SC_ComboBoxListBoxPopup,
                                   this).topLeft());
    const QRect currentItemRect = view()->visualRect(view()->currentIndex());
    int top = view()->mapToGlobal(currentItemRect.topLeft()).y();
    popup->move(popup->x(), popup->y() + above.y() - top);
}
```

(其中 QComboBox 的源代码中, 放置位置的部分感觉其实算法并不十分合理, 我改写了一下)

最终的效果如下: 

![final]({{ site.url }}/figure/2019-01/qcombobox/final.png)
