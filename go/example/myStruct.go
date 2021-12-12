package main

import "fmt"

type Abser interface {
	Abs() float64
}


type AbserPtr interface {
	Abs() float64
}


type Vertex struct {
	X float64
	Y float64
}



type VertexPtr struct {
	X float64
	Y float64
}

func (v Vertex) Abs() float64{
	return v.X + v.Y
}

func (v *VertexPtr) Abs() float64{
	return v.X + v.Y
}

func main()  {
	fmt.Println("---")
	var  a  Abser
	v := Vertex{3, 4}
	fmt.Println(v.Abs())
	a = v
	fmt.Println(a.Abs())
	// 接口是值接收者, 指针也是可以的
	a = &v
	fmt.Println(a.Abs())
	vp := VertexPtr{3, 4}
	fmt.Println(vp.Abs())
	// 指针接收者，只能是指针
	// 	VertexPtr does not implement Abser (Abs method has pointer receiver)
	//a = vp
	// *Vertex 实现了 Abser
	a = &vp
	fmt.Println(a.Abs())
	//a = vp
	//fmt.Println(a.Abs())

	//这个规则说，如果使用指针接收者来实现一个接口，那么只有指向那个类型的指针才能够实现对应的接口。
	//如果使用值接收者来实现一个接口，那么那个类型的值和指针都能够实现对应的接口。
	//用指针接收者实现了接口，但是试图将 user 类型的值传给如果传递的是 user 值的地址，整个程序就能通过编译，并且能够工作了
	//**事实上，编译器并不是总能自动获得一个值的地址**，所以**值的方法集只包括了使用值接收者实现的方法**
}
