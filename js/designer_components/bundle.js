// DesignerComponent.ts
var DesignerComponent = class {
  static postLoad() {
  }
  constructor(container, pyComponent, el) {
    this.domNode = container;
    this.pyComponent = pyComponent;
    this.el = el;
  }
  static init(selector, className = "anvil-extras-designer") {
    const doInit = () => {
      this.loading = true;
      $(() => {
        this.setup(selector, className);
        this.postLoad();
        this.loaded = true;
        this.loading = false;
      });
    };
    if (!this.loaded && !this.loading) {
      this.loading = true;
      this.links.forEach((href) => {
        const l = document.createElement("link");
        l.href = href;
        l.rel = "stylesheet";
        document.body.appendChild(l);
      });
      if (this.css) {
        const s = document.createElement("style");
        s.innerHTML = this.css;
        document.body.appendChild(s);
      }
      if (this.script) {
        const s = document.createElement("script");
        s.src = this.script;
        document.body.appendChild(s);
        s.onload = doInit;
      } else {
        doInit();
      }
    } else if (!this.loading) {
      doInit();
    }
  }
  static setup(selector, className) {
    for (let el of document.querySelectorAll(selector)) {
      const container = el.parentElement;
      if (container.classList.contains(className)) {
        return;
      }
      container.classList.add(className);
      const pyComponent = $(container).data("anvilPyComponent");
      const props = pyComponent._anvil.customPropVals;
      const self = new this(container, pyComponent, el);
      if (props) {
        self.makeGetSets(props);
      }
      self.update({...props || this.defaults});
    }
  }
  makeGetSets(props) {
    const copyProps = {...props};
    const self = this;
    for (let propName in copyProps) {
      this.setProp(propName, props[propName]);
      Object.defineProperty(props, propName, {
        get() {
          return copyProps[propName];
        },
        set(v) {
          copyProps[propName] = v;
          try {
            self.setProp(propName, v);
            self.update({...copyProps}, propName, v);
          } catch {
          }
          return true;
        }
      });
    }
  }
  update(props, propName, val) {
  }
  setProp(propName, val) {
  }
  updateSpacing({spacing_above, spacing_below}) {
    const stale_spacing = Array.prototype.filter.call(this.domNode.classList, (x) => x.startsWith("anvil-spacing-"));
    this.domNode.classList.remove(...stale_spacing);
    spacing_above && this.domNode.classList.add("anvil-spacing-above-" + spacing_above);
    spacing_below && this.domNode.classList.add("anvil-spacing-above-" + spacing_below);
  }
  updateRole({role}) {
    const stale_role = Array.prototype.filter.call(this.domNode.classList, (x) => x.startsWith("anvil-role-"));
    this.domNode.classList.remove(...stale_role);
    role && this.domNode.classList.add("anvil-role-" + role);
  }
  updateVisible({visible}) {
    this.domNode.classList.toggle("visible-false", !visible);
  }
  getColor(color, _default) {
    if (color && color.startsWith("theme:")) {
      color = window.anvilThemeColors[color.replace("theme:", "")] || "";
    }
    if (!color && _default) {
      if (_default === true || _default === "primary") {
        return window.anvilThemeColors["Primary 500"] || "#2196F3";
      }
      return _default;
    }
    return color;
  }
  getColorRGB(color, _default) {
    color = this.getColor(color, _default);
    if (color && color.startsWith("#")) {
      const bigint = parseInt(color.slice(1), 16);
      return [bigint >> 16 & 255, bigint >> 8 & 255, bigint & 255].join(",");
    } else if (color && color.startsWith("rgb(")) {
      return color.slice(4, color.length - 1);
    }
    return color;
  }
  clearElement(el) {
    while (el.firstElementChild) {
      el.removeChild(el.firstElementChild);
    }
  }
  get [Symbol.toStringTag]() {
    return "Designer Component";
  }
};
DesignerComponent.css = "";
DesignerComponent.links = [];
DesignerComponent.script = "";
DesignerComponent.loaded = false;
DesignerComponent.loading = false;
DesignerComponent.defaults = {};
DesignerComponent.initializing = false;

// DesignerMultSelectDropDown.ts
var DesignerMultiSelectDropDown = class extends DesignerComponent {
  static postLoad() {
    $.fn.selectpicker.Constructor.BootstrapVersion = "3";
  }
  static init() {
    super.init(".select-picker");
  }
  constructor(domNode, pyComponent, select) {
    super(domNode, pyComponent, select);
    this.picker = $(select);
    this.picker.selectpicker();
  }
  update(props, propName) {
    if (propName && !(propName in this.constructor.defaults)) {
      return;
    }
    this.picker.attr("title", props["placeholder"] || null);
    this.picker.selectpicker({title: props["placeholder"]});
    this.picker.attr("disabled", props["enabled"] ? null : "");
    this.updateSpacing(props);
    this.updateVisible(props);
    this.picker.selectpicker("refresh");
    this.picker.selectpicker("render");
  }
};
DesignerMultiSelectDropDown.defaults = {
  placeholder: "None Selected",
  enabled: true,
  visible: true,
  spacing_above: "small",
  spacing_below: "small"
};
DesignerMultiSelectDropDown.links = ["https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/css/bootstrap-select.min.css"];
DesignerMultiSelectDropDown.script = "https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/js/bootstrap-select.min.js";

// DesignerQuill.ts
var DesignerQuill = class extends DesignerComponent {
  static init() {
    super.init(".quill-editor");
  }
  constructor(domNode, pyComponent, editor) {
    super(domNode, pyComponent, editor);
    this.editor = editor;
  }
  update(props) {
    if (this.editor.firstElementChild) {
      this.editor.removeChild(this.editor.firstElementChild);
    }
    if (this.domNode.firstElementChild !== this.editor) {
      this.domNode.removeChild(this.domNode.firstElementChild);
    }
    const q = new Quill(this.editor, {
      modules: {toolbar: props.toolbar || false},
      readOnly: props.readonly,
      theme: props.theme,
      placeholder: props.placeholder
    });
    this.updateSpacing(props);
    this.updateVisible(props);
    let len = props.height;
    len = ("" + len).match(/[a-zA-Z%]/g) ? len : len + "px";
    this.editor.style.minHeight = len;
    this.editor.style.height = props.auto_expand ? len : "auto";
    q.setText(props.content || "");
  }
  get [Symbol.toStringTag]() {
    return "Quill";
  }
};
DesignerQuill.defaults = {
  auto_expand: true,
  content: "",
  height: 150,
  placeholder: null,
  readonly: false,
  theme: "snow",
  toolbar: true,
  visible: true
};
DesignerQuill.links = ["//cdn.quilljs.com/1.3.6/quill.snow.css", "//cdn.quilljs.com/1.3.6/quill.bubble.css"];
DesignerQuill.script = "//cdn.quilljs.com/1.3.6/quill.min.js";

// DesignerSlider.ts
var DesignerSlider = class extends DesignerComponent {
  static init() {
    super.init(".anvil-slider", "anvil-slider-container");
  }
  constructor(domNode, pyComponent, slider) {
    super(domNode, pyComponent, slider);
    this.slider = slider;
  }
  parse(val, force_list = false) {
    if (typeof val !== "string") {
      return val;
    }
    val = val.toLowerCase().trim();
    if (!val)
      return force_list ? [] : null;
    try {
      return JSON.parse((force_list || val.includes(",")) && val[0] !== "[" ? `[${val}]` : val);
    } catch {
      return force_list ? [] : val;
    }
  }
  getFormatter(formatspec) {
    const first = formatspec.indexOf("{");
    const last = formatspec.indexOf("}");
    const prefix = first === -1 ? "" : formatspec.slice(0, first);
    const suffix = last === -1 ? "" : formatspec.slice(last + 1);
    const type = formatspec[last - 1] === "%" ? "%" : null;
    const pyformatspec = Sk.ffi.toPy(formatspec);
    const format = pyformatspec.tp$getattr(Sk.ffi.toPy("format"));
    const do_to = (f) => {
      const pyNum = Sk.ffi.toPy(f);
      return first === -1 ? Sk.builtin.format(pyNum, pyformatspec) : format.tp$call([pyNum]);
    };
    try {
      do_to(1.1);
    } catch (e) {
      throw new Error(e.toString());
    }
    return {
      to: (f) => {
        try {
          return do_to(f);
        } catch {
          return f;
        }
      },
      from: (s) => {
        if (s.startsWith(prefix)) {
          s = s.slice(prefix.length);
        }
        if (s.endsWith(suffix)) {
          s = s.slice(0, s.length - suffix.length);
        }
        const has_percent = type === "%" && s.endsWith("%");
        s = s.trim().replace(/[,_]/g, "");
        let f = parseFloat(s);
        if (has_percent) {
          f = f / 100;
        }
        return f;
      }
    };
  }
  update(props) {
    try {
      for (let prop of ["start", "connect", "margin", "padding", "limit", "pips_values"]) {
        props[prop] = this.parse(props[prop], prop === "pips_values");
      }
      props.range = {min: props.min, max: props.max};
      props.format = this.getFormatter(props.format || ".2f");
      if (props.pips) {
        props.pips = {
          format: props["format"],
          mode: props["pips_mode"],
          values: props["pips_values"],
          density: props["pips_density"],
          stepped: props["pips_stepped"]
        };
      }
      this.domNode.classList.toggle("has-pips", !!props.pips);
      this.slider.noUiSlider?.destroy();
      if (this.slider.firstElementChild) {
        this.slider.removeChild(this.slider.firstElementChild);
      }
      this.domNode.style.setProperty("--primary", this.getColor(props.color, true));
      this.updateSpacing(props);
      this.updateVisible(props);
      props.enabled ? this.slider.removeAttribute("disabled") : this.slider.setAttribute("disabled", "");
      noUiSlider.create(this.slider, props);
    } catch (e) {
      this.slider.noUiSlider?.destroy();
      if (this.slider.firstElementChild) {
        this.slider.removeChild(this.slider.firstElementChild);
      }
      const invalidComponent = $(`<div class='invalid-component'>
              <i class="glyphicon glyphicon-remove"></i>
              <div class="err">${e.message.replaceAll("noUiSlider", "Slider")}</div></div>`);
      this.slider.appendChild(invalidComponent[0]);
    }
  }
  get [Symbol.toStringTag]() {
    return "Slider";
  }
};
DesignerSlider.defaults = {
  start: [20, 80],
  connect: true,
  min: 0,
  max: 100,
  visible: true,
  enabled: true
};
DesignerSlider.links = ["https://cdn.jsdelivr.net/npm/nouislider@15.1.1/dist/nouislider.css"];
DesignerSlider.script = "https://cdn.jsdelivr.net/npm/nouislider@15.1.1/dist/nouislider.js";
DesignerSlider.css = `.anvil-container-overflow,.anvil-panel-col{overflow:visible}.anvil-slider-container{padding:10px 0;min-height:50px}
.anvil-slider-container.has-pips{padding-bottom:40px}.noUi-connect{background:var(--primary)}
.noUi-horizontal .noUi-handle{width:34px;height:34px;right:-17px;top:-10px;border-radius:50%}.noUi-handle::after,.noUi-handle::before{content:none}`;

// DesignerSwitch.ts
var DesignerSwitch = class extends DesignerComponent {
  static init() {
    super.init(".anvil-extras-switch");
  }
  constructor(domNode, pyComponent, el) {
    super(domNode, pyComponent, el);
    const cb = pyComponent._anvil.components[0].component;
    const cbNode = cb._anvil.domNode;
    cbNode.classList.add("switch");
    cbNode.style.setProperty("--color", this.getColorRGB("#2196F3"));
    const span = cbNode.querySelector("span");
    span.classList.add("lever");
    span.removeAttribute("style");
    const label = cbNode.querySelector("label");
    const textNodePre = document.createTextNode("");
    const textNodePost = document.createTextNode("");
    label.prepend(textNodePre);
    label.append(textNodePost);
    label.style.padding = "7px 0";
    this.cb = cb;
    this.cbNode = cbNode;
    this.textNodePre = textNodePre;
    this.textNodePost = textNodePost;
  }
  setProp(propName, v) {
    try {
      this.cb._anvil.setProp(propName, Sk.ffi.toPy(v));
    } catch (e) {
      if (propName === "checked_color") {
        this.cbNode.style.setProperty("--color", this.getColorRGB(v, true));
      } else if (propName === "text_pre") {
        this.textNodePre.textContent = v;
      } else {
        this.textNodePost.textContent = v;
      }
    }
  }
  get [Symbol.toStringTag]() {
    return "Switch";
  }
};
DesignerSwitch.css = `
.switch,.switch *{-webkit-tap-highlight-color:transparent;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}
.switch label{cursor:pointer}
.switch label input[type=checkbox]{opacity:0;width:0;height:0}.switch label input[type=checkbox]:checked+.lever{background-color:rgba(var(--color), .5)}
.switch label input[type=checkbox]:checked+.lever:after,.switch label input[type=checkbox]:checked+.lever:before{left:18px}
.switch label input[type=checkbox]:checked+.lever:after{background-color:rgb(var(--color))}
.switch label .lever{content:"";display:inline-block;position:relative;width:36px;height:14px;background-color:rgba(0,0,0,0.38);border-radius:15px;margin-right:10px;-webkit-transition:background 0.3s ease;transition:background 0.3s ease;vertical-align:middle;margin:0 16px}
.switch label .lever:after,.switch label .lever:before{content:"";position:absolute;display:inline-block;width:20px;height:20px;border-radius:50%;left:0;top:-3px;-webkit-transition:left 0.3s ease, background 0.3s ease, -webkit-box-shadow 0.1s ease, -webkit-transform 0.1s ease;transition:left 0.3s ease, background 0.3s ease, -webkit-box-shadow 0.1s ease, -webkit-transform 0.1s ease;transition:left 0.3s ease, background 0.3s ease, box-shadow 0.1s ease, transform 0.1s ease;transition:left 0.3s ease, background 0.3s ease, box-shadow 0.1s ease, transform 0.1s ease, -webkit-box-shadow 0.1s ease, -webkit-transform 0.1s ease}
.switch label .lever:before{background-color:rgb(var(--color), 0.15)}
.switch label .lever:after{background-color:#F1F1F1;-webkit-box-shadow:0 3px 1px -2px rgba(0,0,0,0.2),0px 2px 2px 0 rgba(0,0,0,0.14),0px 1px 5px 0 rgba(0,0,0,0.12);box-shadow:0 3px 1px -2px rgba(0,0,0,0.2),0px 2px 2px 0 rgba(0,0,0,0.14),0px 1px 5px 0 rgba(0,0,0,0.12)}
input[type=checkbox]:checked:not(:disabled) ~ .lever:active::before,input[type=checkbox]:checked:not(:disabled).tabbed:focus ~ .lever::before{-webkit-transform:scale(2.4);transform:scale(2.4);background-color:rgb(var(--color), 0.15)}
input[type=checkbox]:not(:disabled) ~ .lever:active:before,input[type=checkbox]:not(:disabled).tabbed:focus ~ .lever::before{-webkit-transform:scale(2.4);transform:scale(2.4);background-color:rgba(0,0,0,0.08)}
.switch input[type=checkbox][disabled]+.lever{cursor:default;background-color:rgba(0,0,0,0.12)}
.switch label input[type=checkbox][disabled]+.lever:after,.switch label input[type=checkbox][disabled]:checked+.lever:after{background-color:#949494}`;

// DesignerTabs.ts
var DesignerTabs = class extends DesignerComponent {
  static init() {
    super.init(".anvil-container .tabs", "anvil-extras-designer");
  }
  constructor(domNode, pyComponent, el) {
    super(domNode, pyComponent, el);
    this.tabs = el;
    this.domNode.style.paddingTop = "0";
    this.domNode.style.paddingBottom = "0";
  }
  update(props) {
    this.clearElement(this.tabs);
    let active = {offsetLeft: 0, offsetWidth: 0};
    props.tab_titles ||= [];
    props.tab_titles.forEach((title, i) => {
      const li = document.createElement("li");
      li.className = "tab";
      const a = document.createElement("a");
      a.style.cssText = `
			font-weight:${props.bold ? "bold" : ""};
			text-align: ${props.align};
			font-size: ${props.font_size ? props.font_size + "px" : ""};
			font-family:${props.font || ""};
			font-style: ${props.italic ? "italic" : ""};
			`;
      a.textContent = title;
      li.appendChild(a);
      this.tabs.appendChild(li);
      if (i === props.active_tab_index) {
        a.className = "active";
        active = li;
      }
    });
    const indicator = document.createElement("li");
    this.tabs.appendChild(indicator);
    indicator.className = "indicator";
    indicator.style.left = active.offsetLeft + "px";
    indicator.style.right = this.tabs.offsetWidth - active.offsetLeft - active.offsetWidth + "px";
    const fg = this.getColorRGB(props.foreground, true);
    this.tabs.style.setProperty("--color", fg);
    const bg = this.getColor(props.background);
    this.tabs.style.setProperty("--background", bg);
    this.updateSpacing(props);
    this.updateRole(props);
    this.updateVisible(props);
  }
  get [Symbol.toStringTag]() {
    return "Tabs";
  }
};
DesignerTabs.defaults = {tab_titles: ["Tab 1", "Tab 2"], active_tab_index: 0, visible: true, align: "left"};
DesignerTabs.css = `.tabs{position:relative;overflow-x:auto;overflow-y:hidden;height:48px;width:100%;background-color:var(--background, inherit);margin:0 auto;white-space:nowrap;padding:0;display:flex}
.tabs .tab{flex-grow:1;display:inline-block;text-align:center;line-height:48px;height:48px;padding:0;margin:0;text-transform:uppercase}
.tabs .tab a{color:rgba(var(--color),0.7);display:block;width:100%;height:100%;padding:0 24px;font-size:14px;text-overflow:ellipsis;overflow:hidden;-webkit-transition:color 0.28s ease, background-color 0.28s ease;transition:color 0.28s ease, background-color 0.28s ease}
.tabs .tab a:focus,.tabs .tab a:focus.active{background-color:rgb(var(--color), 0.2);outline:none}
.tabs .tab a.active,.tabs .tab a:hover{background-color:transparent;color:rgb(var(--color))}
.tabs .indicator{position:absolute;bottom:0;height:3px;background-color:rgb(var(--color), 0.4);will-change:left, right}`;
export {
  DesignerMultiSelectDropDown,
  DesignerQuill,
  DesignerSlider,
  DesignerSwitch,
  DesignerTabs
};
