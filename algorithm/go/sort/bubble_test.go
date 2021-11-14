package sort

import (
    "fmt"
    "testing"
)

func TestBubbleSort(t *testing.T) {

    list := []int{3, 2, 1}
    BubbleSort(list)

    for i := 0; i < len(list)-2; i++ {
        if list[i] > list[i+1] {
            fmt.Println(list)
            t.Error()
        }
    }
}
