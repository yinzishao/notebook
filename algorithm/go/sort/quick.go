package sort

import (
    "fmt"
)

func QuickSort(arr []int) {
    fmt.Println(arr)
    qSort(arr, 0, len(arr)-1)
    fmt.Println(arr)
}

func qSort(arr []int, l int, r int) {
    if l < r {
        //p := partition(arr, l, r)
        p := partition2(arr, l, r)
        //p := partition3(arr, l, r)
        //p := partition4(arr, l, r)
        qSort(arr, l, p-1)
        qSort(arr, p+1, r)
    }
}

/*
执行用时：24 ms, 在所有 Go 提交中击败了87.12%的用户
内存消耗：6.2 MB, 在所有 Go 提交中击败了96.15%的用户
 */
func partition(arr []int, l int, r int) int {
    // 最后一个作为基准
    pivotkey := arr[r]
    for ; l < r; {
        // 左边进行循环，得到一个比基准大的，则停止。l停留在比基准值大的下标处
        for ; l < r && arr[l] <= pivotkey; {
            l++
        }
        // 交换左边（比基准值大）与右边（比基准值小）
        arr[r] = arr[l]
        //注意不需要--
        //r --
        //右边循环找到比基准值小的，r停留在比基准值小的下标处
        for ; l < r && arr[r] >= pivotkey; {
            r--
        }
        // 交换左边（循环得到的比基准值大的下标）与右边（循环得到的比基准值小的下标）
        arr[l] = arr[r]
        //注意不需要加加，最后就是l？为什么呢？最后l==r。
        //l ++
    }
    arr[l] = pivotkey
    return l
}

// 或者换个思路？
// 往左找到比基准大的，往右找到比基准小的，然后交换。直到相交。这个思路比较清晰，但怎么将交值和基准值交换呢？需要比较基准值与中间值，后判断中间的值往前交换还是往后交换才行。没写出来。
// 参考partition4更新： 注意往中间缩的先后顺序就可以了
func partition2(arr []int, l int, r int) int  {
    /*
    执行用时：24 ms, 在所有 Go 提交中击败了87.12%的用户
    内存消耗：6.2 MB, 在所有 Go 提交中击败了88.26%的用户
     */
    pivotkey := arr[l]
    tmp := l
    for ; l < r; {
        // 后先。可以保证l下标的值是比基准值要小的
        for ; l < r && arr[r] >= pivotkey; {
            r--
        }
        for ; l < r && arr[l] <= pivotkey; {
            l++
        }
        arr[l], arr[r] = arr[r], arr[l]
    }
    arr[tmp], arr[l] = arr[l], arr[tmp]
    return l
}

/*
执行用时：24 ms, 在所有 Go 提交中击败了87.12%的用户
内存消耗：6.2 MB, 在所有 Go 提交中击败了96.15%的用户
 */
func partition3(arr []int, l int, r int) int {
    // 参考Python写的版本，不过这次把基准值设为最左边
    // 从右往左遍历的永远递减下标j（遍历数组），**需要一个临时游标记录i（记录需要填坑的游标， i的右边永远符合规则：比基准值大）**。
    //（基准值是最左边的时候，从左往右遍历行不行？）
    // 1. 当j下标的数值比基准值大的时候，**交换i与j，i--（一开始是等位置的交换）**。
    // 2. 当j下标的数值比基准值小的时候，**i不动（这个值比基准值小），以此定位i的需要交换的下标**。
    // [5, 8, 7, 2, 1] => [5, 8, 1, 2, 7] => [5, 2, 1, 8, 7] => [1, 2, 5, 8, 7]

    p := arr[l]
    i := r
    for j := r; j > l; j -- {
        if arr[j] > p {
            arr[j], arr[i] = arr[i], arr[j]
            i --
        }
    }
    arr[l], arr[i] = arr[i], arr[l]
    return i
}

// 取中值优化
/*
执行用时：24 ms, 在所有 Go 提交中击败了87.12%的用户
内存消耗：6.3 MB, 在所有 Go 提交中击败了57.98%的用户
 */
func partition4(arr []int, l int, r int) int {
    var m = l + (r - l) /2
    if arr[l] > arr[r] {  //保证左端较小
        arr[l], arr[r] = arr[r], arr[l]
    }
    if arr[m] > arr[r] {  //保证中间较小
        arr[m], arr[r] = arr[r], arr[m]
    }
    if arr[m] > arr[l] {  //保证左端为中值
        arr[m], arr[l] = arr[l], arr[m]
    }
    //此时array[low]已经为整个序列左中右三个关键字的中间值
    pivotkey := arr[l]
    t := l
    for ; l < r; {

        // 注意这里从后遍历，再往前遍历！！
        // 换顺序会有错误。因为从后面遍历，可以保证l下标的值是比基准值要小的。
        for ; l < r && arr[r] >= pivotkey; {
            r--
        }

        for ; l < r && arr[l] <= pivotkey; {
            l++
        }

        if l < r {
            arr[l], arr[r] = arr[r], arr[l]
        }
    }
    arr[t], arr[l] = arr[l], arr[t]
    return l

}
