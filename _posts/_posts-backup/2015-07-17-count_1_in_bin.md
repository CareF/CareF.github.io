---
title: 数二进制表示中有多少1的算法
date: '2015-07-17 11:39:00 -0400'
categories:
- Math
tags: [data processing, algorithm]
---
最早在邓公的数据结构书上看到, 当时只是觉得很有趣, 没想到竟然会要用上, 于是来记一笔:

先说用途: Heat Bath Algorithmic Cooling 中, 有一个步骤是把 $$ n $$ 个 qubit 扔到热库中变成热平衡. 此时得到的密度矩阵矩阵是对角的, 对角元 $$ (1+\varepsilon)^i(1-\varepsilon)^{n-i} $$ 其中 $$ i $$ 为对应的态中处于基态的 qubit 数目: 恰好为矩阵行数\列数在二进制表示下 0 的数目.

算法有个名称叫做 Hamming weight, 以下程序摘抄自 Wiki

<pre><code>\\types and constants used in the functions below

const uint64_t m1  = 0x5555555555555555; \\binary: 0101...
const uint64_t m2  = 0x3333333333333333; \\binary: 00110011..
const uint64_t m4  = 0x0f0f0f0f0f0f0f0f; \\binary:  4 zeros,  4 ones ...
const uint64_t m8  = 0x00ff00ff00ff00ff; \\binary:  8 zeros,  8 ones ...
const uint64_t m16 = 0x0000ffff0000ffff; \\binary: 16 zeros, 16 ones ...
const uint64_t m32 = 0x00000000ffffffff; \\binary: 32 zeros, 32 ones
const uint64_t hff = 0xffffffffffffffff; \\binary: all ones
const uint64_t h01 = 0x0101010101010101; \\the sum of 256 to the power of 0,1,2,3...

\\This is a naive implementation, shown for comparison,
\\and to help in understanding the better functions.
\\It uses 24 arithmetic operations (shift, add, and).
int popcount_1(uint64_t x) {
    x = (x &amp; m1 ) + ((x >>  1) &amp; m1 ); \\put count of each  2 bits into those  2 bits
    x = (x &amp; m2 ) + ((x >>  2) &amp; m2 ); \\put count of each  4 bits into those  4 bits
    x = (x &amp; m4 ) + ((x >>  4) &amp; m4 ); \\put count of each  8 bits into those  8 bits
    x = (x &amp; m8 ) + ((x >>  8) &amp; m8 ); \\put count of each 16 bits into those 16 bits
    x = (x &amp; m16) + ((x >> 16) &amp; m16); \\put count of each 32 bits into those 32 bits
    x = (x &amp; m32) + ((x >> 32) &amp; m32); \\put count of each 64 bits into those 64 bits
    return x;
}

\\This uses fewer arithmetic operations than any other known
\\implementation on machines with slow multiplication.
\\It uses 17 arithmetic operations.
int popcount_2(uint64_t x) {
    x -= (x >> 1) &amp; m1;             \\put count of each 2 bits into those 2 bits
    x = (x &amp; m2) + ((x >> 2) &amp; m2); \\put count of each 4 bits into those 4 bits
    x = (x + (x >> 4)) &amp; m4;        \\put count of each 8 bits into those 8 bits
    x += x >>  8;  \\put count of each 16 bits into their lowest 8 bits
    x += x >> 16;  \\put count of each 32 bits into their lowest 8 bits
    x += x >> 32;  \\put count of each 64 bits into their lowest 8 bits
    return x &amp; 0x7f;
}

\\This uses fewer arithmetic operations than any other known
\\implementation on machines with fast multiplication.
\\It uses 12 arithmetic operations, one of which is a multiply.
int popcount_3(uint64_t x) {
    x -= (x >> 1) &amp; m1;             \\put count of each 2 bits into those 2 bits
    x = (x &amp; m2) + ((x >> 2) &amp; m2); \\put count of each 4 bits into those 4 bits
    x = (x + (x >> 4)) &amp; m4;        \\put count of each 8 bits into those 8 bits
    return (x * h01)>>56;  \\returns left 8 bits of x + (x<<8) + (x<<16) + (x<<24) + ...
}
<\code><\pre>

