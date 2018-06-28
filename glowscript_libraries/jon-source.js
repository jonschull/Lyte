// backtick  v
var source = `
#these lines comes from jonsource.js 
b=box(color=color.yellow)
c=cone(color=color.red)
expand=True
for i in range(20):
    expand = not expand
    for i in range(20):
        if expand:
            c.radius += 0.1
        else:
            c.radius -= 0.1
        scene.waitfor('redraw')


`
//backtick