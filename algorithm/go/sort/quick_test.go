package sort

import (
    "fmt"
    "math/rand"
    "testing"
)

func TestQuickSort(t *testing.T) {

    for j := 0; j < 10000; j++ {
      var list []int
      for i := 0; i < 10; i++ {
          list = append(list, rand.Intn(100))
      }
      //list := []int{8, 9 , 5, 3, 2, 1}
      QuickSort(list)

      for i := 0; i < len(list)-2; i++ {
          if list[i] > list[i+1] {
              fmt.Println(list)
              t.Error()
          }
      }
    }

    //list := []int{1, 2, 3}
    list := []int{5, 8, 7, 2, 1}
    QuickSort(list)

    for i := 0; i < len(list)-2; i++ {
        if list[i] > list[i+1] {
            fmt.Println(list)
            t.Error()
        }
    }
}
