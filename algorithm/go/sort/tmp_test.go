package sort

import (
    "fmt"
    "math/rand"
    "testing"
    "time"
)

func sortArray(nums []int) []int {
    l := len(nums)

    for i := 0; i < l-1; i += 1 {
        for j := 0; j < (l - i - 1); j += 1 {
            if nums[j+1] < nums[j] {
                nums[j+1], nums[j] = nums[j], nums[j+1]
            }
        }
    }

    return nums
}

func genRandomList(len int) []int {
    var list []int
    for i := 0; i < len; i += 1 {
        list = append(list, rand.Intn(len))
    }
    return list
}

func CheckList(list []int) {
    for i := 0; i < len(list)-2; i++ {
        if list[i] > list[i+1] {
            fmt.Println(list)
            panic("crash")
        }
    }
}

func TestTmp(t *testing.T) {
    list := genRandomList(10)
    fmt.Printf("before %v\n", list)
    list = sortArray(list)
    fmt.Printf("after %v\n", list)
    CheckList(list)
}

func yufa() {
    rand.Seed(time.Now().Unix())
    fmt.Println(rand.Perm(10))
    fmt.Println(rand.Intn(100))
    // 声明切片
    var list []int
    // []
    fmt.Println(list)
    // 追加
    list = append(list, 12, 123)
    // [12, 123]
    fmt.Println(list)

    slice1 := make([]int, 5)
    // [0 0 0 0 0]
    fmt.Println(slice1)
    list = make([]int, 0)
    for i := 0; i < 100; i += 1 {
        list = append(list, rand.Intn(100))
    }
    fmt.Println(list)

    // 格式化： https://www.cnblogs.com/rickiyang/p/11074171.html
    fmt.Printf("format %v\n", list)

}
