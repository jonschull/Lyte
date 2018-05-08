(function() { var __rt=srequire('streamline/lib/callbacks/runtime').runtime(__filename, false),__func=__rt.__func; var RS_modules = {};
RS_modules.pythonize = {};

(function() {
  function strings() {
    var string_funcs, exclude, name;
    string_funcs = set("capitalize strip lstrip rstrip islower isupper isspace lower upper swapcase center count endswith startswith find rfind index rindex format join ljust rjust partition rpartition replace split rsplit splitlines zfill".split(" "));
    if (!arguments.length) {
      exclude = (function() {
        var s = RS_set();
        s.jsset.add("split");
        s.jsset.add("replace");
        return s;
      })(); }
     else if (arguments[0]) {
      exclude = Array.prototype.slice.call(arguments); }
     else {
        exclude = null;
    }
      if (exclude) {
        string_funcs = string_funcs.difference(set(exclude));
    }
      var RS_Iter0 = RS_Iterable(string_funcs);
    for (var RS_Index0 = 0; RS_Index0["<"](RS_Iter0.length); RS_Index0++) {
      name = RS_Iter0[RS_Index0];
        (RS_expr_temp = String.prototype)[((((typeof name === "number") && name["<"](0))) ? RS_expr_temp.length["+"](name) : name)] = (RS_expr_temp = RS_str.prototype)[((((typeof name === "number") && name["<"](0))) ? RS_expr_temp.length["+"](name) : name)];
    }
  }
    RS_modules.pythonize.strings = strings;
})();
function main(_) { var version, box, sphere, cylinder, pyramid, cone, helix, ellipsoid, ring, arrow, compound, display, vector, print, scene, RS_ls, __name__, strings;
function GlowMe() {
var me = ((((arguments[0] === undefined) || (((((0 === arguments.length["-"](1)) && (arguments[arguments.length["-"](1)] !== null)) && (typeof arguments[arguments.length["-"](1)] === "object")) && (arguments[arguments.length["-"](1)][RS_kwargs_symbol] === true))))) ? GlowMe.__defaults__.me : arguments[0]);
var RS_kwargs_obj = arguments[arguments.length["-"](1)];
  if ((((RS_kwargs_obj === null) || (typeof RS_kwargs_obj !== "object")) || (RS_kwargs_obj[RS_kwargs_symbol] !== true))) {
      RS_kwargs_obj = {};
  }
  if (Object.prototype.hasOwnProperty.call(RS_kwargs_obj, "me")) {
    me = RS_kwargs_obj.me;
}
}
function f() {
  var RS_ls;
  print("this is a function");
}
var __frame = { name: "main", line: 32 };


return __func(_, this, arguments, main, 0, __frame, function __$main() { version = RS_list_decorate(["2.7","glowscript",]); Array.prototype["+"] = function(r) { return this.concat(r); };
Array.prototype["*"] = function(r) { return __array_times_number(this, r); }; __name__ = "__main__";
window.__GSlang = "vpython";
box = vp_box;
sphere = vp_sphere;
cylinder = vp_cylinder;
pyramid = vp_pyramid;
cone = vp_cone;
helix = vp_helix;
ellipsoid = vp_ellipsoid;
ring = vp_ring;
arrow = vp_arrow;
compound = vp_compound;
display = canvas;
vector = vec;
print = GSprint;
scene = canvas();
strings = RS_modules.pythonize.strings;
strings();

    if (!GlowMe.__defaults__) {
        Object.defineProperties(GlowMe, {
            __defaults__: {value: {me: ""}},
            __handles_kwarg_interpolation__: {value: true},
            __argnames__: {value: ["me",]}
        });
    }
    eval(MYVP)
});
}
if (!main.__argnames__) { Object.defineProperties(main, {
__argnames__: {value: ["_",]}
});
}
    $(function () {
        window.__context = {glowscript_container: $("#glowscript").removeAttr("id")};
        main(__func)
    })
})();
