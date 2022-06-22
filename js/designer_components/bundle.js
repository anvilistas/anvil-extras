// DesignerComponent.ts
var HASUNITS = /[a-zA-Z%]/g;
var DesignerComponent = class {
  constructor(domNode, pyComponent, el) {
    this.domNode = domNode;
    this.pyComponent = pyComponent;
    this.el = el;
    this.domNode = domNode;
    this.pyComponent = pyComponent;
    this.el = el;
  }
  static postLoad() {
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
      if (this.scripts.length) {
        const promises = this.scripts.map((script) => new Promise((resolve, reject) => {
          const s = document.createElement("script");
          s.src = script;
          document.body.appendChild(s);
          s.onload = resolve;
          s.onerror = reject;
        }));
        Promise.all(promises).then(doInit);
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
      let props;
      try {
        props = pyComponent._anvil.customPropVals;
      } catch (e) {
        console.error(e);
        return;
      }
      const self = new this(container, pyComponent, el);
      if (props) {
        self.makeGetSets(props);
      } else if (this.defaults) {
        self.update({...this.defaults});
        for (let [propName, propVal] of Object.entries(this.defaults)) {
          self.setProp(propName, propVal, this.defaults);
        }
      }
    }
  }
  makeGetSets(props) {
    const copyProps = {...props};
    const self = this;
    this.update({...copyProps});
    for (let propName in copyProps) {
      this.setProp(propName, props[propName], copyProps);
      Object.defineProperty(props, propName, {
        get() {
          return copyProps[propName];
        },
        set(v) {
          copyProps[propName] = v;
          try {
            self.setProp(propName, v, copyProps);
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
  setProp(propName, val, props) {
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
  getCssLength(len) {
    len ??= "";
    return ("" + len).match(HASUNITS) ? len : len + "px";
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
DesignerComponent.scripts = [];
DesignerComponent.loaded = false;
DesignerComponent.loading = false;
DesignerComponent.defaults = null;
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
    this.picker.data("width", props["width"]);
    this.picker.attr("disabled", props["enabled"] ? null : "");
    this.updateSpacing(props);
    this.updateVisible(props);
    this.picker.selectpicker("refresh");
    this.picker.selectpicker("render");
  }
  get [Symbol.toStringTag]() {
    return "MultiSelectDropDown";
  }
};
DesignerMultiSelectDropDown.defaults = {
  placeholder: "None Selected",
  enabled: true,
  visible: true,
  width: "",
  spacing_above: "small",
  spacing_below: "small"
};
DesignerMultiSelectDropDown.links = ["https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/css/bootstrap-select.min.css"];
DesignerMultiSelectDropDown.scripts = ["https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.18/dist/js/bootstrap-select.min.js"];

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
DesignerQuill.scripts = ["//cdn.quilljs.com/1.3.6/quill.min.js"];

// DesignerSlider.ts
var BAR_COLOR = "--slider-bar-color";
var BAR_HEIGHT = "--slider-height";
var HANDLE_SIZE = "--slider-handle-size";
var DesignerSlider = class extends DesignerComponent {
  static init() {
    super.init(".anvil-slider", "anvil-slider-container");
  }
  constructor(domNode, pyComponent, slider) {
    super(domNode, pyComponent, slider);
    this.slider = slider;
  }
  parse(val, forceList = false) {
    if (typeof val !== "string") {
      return val;
    }
    val = val.toLowerCase().trim();
    if (!val)
      return forceList ? [] : null;
    try {
      return JSON.parse((forceList || val.includes(",")) && val[0] !== "[" ? `[${val}]` : val);
    } catch {
      return forceList ? [] : val;
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
    const doTo = (f) => {
      const pyNum = Sk.ffi.toPy(f);
      return first === -1 ? Sk.builtin.format(pyNum, pyformatspec) : format.tp$call([pyNum]);
    };
    try {
      doTo(1.1);
    } catch (e) {
      throw new Error(e.toString());
    }
    return {
      to: (f) => {
        try {
          return doTo(f);
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
        const hasPercent = type === "%" && s.endsWith("%");
        s = s.trim().replace(/[,_]/g, "");
        let f = parseFloat(s);
        if (hasPercent) {
          f = f / 100;
        }
        return f;
      }
    };
  }
  update(props) {
    try {
      for (const prop of ["start", "connect", "margin", "padding", "limit", "pips_values"]) {
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
      this.domNode.style.setProperty(BAR_COLOR, this.getColor(props.color, true));
      this.updateSpacing(props);
      this.updateVisible(props);
      this.updateRole(props);
      const barHeight = this.getCssLength(props.bar_height || 18);
      const handleSize = this.getCssLength(props.handle_size || 34);
      this.domNode.style.setProperty(BAR_HEIGHT, barHeight);
      this.domNode.style.setProperty(HANDLE_SIZE, handleSize);
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
DesignerSlider.links = ["https://cdn.jsdelivr.net/npm/nouislider@15.4.0/dist/nouislider.css"];
DesignerSlider.scripts = ["https://cdn.jsdelivr.net/npm/nouislider@15.4.0/dist/nouislider.js"];
DesignerSlider.css = `.anvil-slider-container{padding:10px 0}.anvil-slider-container.has-pips{padding-bottom:40px}
    .anvil-container-overflow,.anvil-panel-col{overflow:visible}.noUi-connect{background:var(${BAR_COLOR})}
    .noUi-horizontal{height:var(${BAR_HEIGHT})}
    .noUi-horizontal .noUi-handle{width:var(${HANDLE_SIZE});height:var(${HANDLE_SIZE});right:calc(var(${HANDLE_SIZE}) / -2);top:calc((-2px + var(${BAR_HEIGHT}) - var(${HANDLE_SIZE}))/2);border-radius:50%}
    .noUi-handle::after,.noUi-handle::before{content:none}`;

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
  setProp(propName, v, props) {
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
DesignerTabs.css = `.anvil-extras-tabs.anvil-role-card{border-bottom-left-radius:0;border-bottom-right-radius:0;margin-bottom:-1px}.tabs{position:relative;overflow-x:auto;overflow-y:hidden;height:48px;width:100%;background-color:var(--background, inherit);margin:0 auto;white-space:nowrap;padding:0;display:flex;z-index:1}.tabs .tab{flex-grow:1;display:inline-block;text-align:center;line-height:48px;height:48px;padding:0;margin:0;text-transform:uppercase}.tabs .tab a{color:rgba(var(--color),0.7);display:block;width:100%;height:100%;padding:0 24px;font-size:14px;text-overflow:ellipsis;overflow:hidden;-webkit-transition:color 0.28s ease, background-color 0.28s ease;transition:color 0.28s ease, background-color 0.28s ease}.tabs .tab a:focus,.tabs .tab a:focus.active{background-color:rgb(var(--color), 0.2);outline:none}.tabs .tab a.active,.tabs .tab a:hover{background-color:transparent;color:rgb(var(--color))}.tabs .indicator{position:absolute;bottom:0;height:3px;background-color:rgb(var(--color), 0.4);will-change:left, right}`;

// DesignerChips.ts
var DesignerChip = class extends DesignerComponent {
  static init() {
    super.init(".chip-placeholder", "anvil-extras-chip");
  }
  constructor(container, pyComponent, temp) {
    super(container, pyComponent, temp);
    temp.remove();
    this.label = pyComponent._anvil.components[0].component;
    this.link = pyComponent._anvil.components[1].component;
    this.linkNode = this.link._anvil.domNode;
    this.linkNode.classList.remove("anvil-container");
  }
  setProp(propName, propVal, props) {
    switch (propName) {
      case "visible":
        this.updateVisible(props);
        break;
      case "spacing_above":
      case "spacing_below":
        this.updateSpacing(props);
        break;
      case "text":
      case "icon":
        this.label._anvil.setPropJS(propName, propVal);
        break;
      case "foreground":
        this.link._anvil.setPropJS(propName, propVal || "rgba(0,0,0,0.6)");
        this.label._anvil.setPropJS(propName, propVal || "rgba(0,0,0,0.6)");
        break;
      case "close_icon":
        this.linkNode.style.display = propVal ? "block" : "none";
        break;
      case "background":
        this.pyComponent._anvil.setPropJS(propName, propVal);
        break;
    }
  }
  get [Symbol.toStringTag]() {
    return "Chip";
  }
};
DesignerChip.css = `.anvil-extras-chip{height:32px;font-size:14px;font-weight:500;color:rgba(0,0,0,0.6);line-height:32px;padding:0 12px;border-radius:16px;background-color:#e4e4e4;cursor:pointer;display:flex;gap:14px;align-items:center;width:fit-content;padding-left:12px;padding-right:12px}.anvil-extras-chip i.anvil-component-icon.left{font-size:1.5rem}.anvil-extras-chip a{user-select:none}.anvil-extras-chip a .link-text{}.anvil-extras-chip span{padding:0 !important}`;
var DesignerChipsInput = class extends DesignerComponent {
  static init() {
    DesignerChip.init();
    super.init(".chips-input-placeholder", "anvil-extras-chips-input");
  }
  constructor(container, pyComponent, temp) {
    super(container, pyComponent, temp);
    temp.remove();
    const tempChip = pyComponent._anvil.components[0].component;
    this.chipNode = tempChip._anvil.domNode;
    this.input = pyComponent._anvil.components[1].component;
    this.inputNode = this.input._anvil.domNode;
    this.chips = [];
    Sk.misceval.callsimArray(tempChip.tp$getattr(new Sk.builtin.str("remove_from_parent")));
  }
  setProp(propName, propVal, props) {
    switch (propName) {
      case "chips":
        debugger;
        propVal = Array.from(new Set((propVal || []).filter((t) => t)));
        this.chips.forEach((chip) => this.domNode.removeChild(chip));
        this.chips = [];
        propVal.forEach((text, i) => {
          const newNode = this.chipNode.cloneNode(true);
          newNode.querySelector("span").textContent = text;
          this.chips.push(newNode);
          this.domNode.insertBefore(newNode, this.inputNode);
        });
        this.chips.length ? this.input._anvil.setPropJS("placeholder", props.secondary_placeholder) : this.input._anvil.setPropJS("placeholder", props.primary_placeholder);
        break;
      case "spacing_above":
      case "spacing_below":
        this.updateSpacing(props);
        break;
      case "visible":
        this.updateVisible(props);
        break;
      case "primary_placeholder":
        !this.chips.length && this.input._anvil.setPropJS("placeholder", propVal);
        break;
      case "secondary_placeholder":
        this.chips.length && this.input._anvil.setPropJS("placeholder", propVal);
        break;
    }
  }
  get [Symbol.toStringTag]() {
    return "ChipsInput";
  }
};
DesignerChipsInput.css = `.anvil-extras-chips-input input{box-shadow:none !important;border:none !important;padding:7px 0 !important;margin-bottom:0 !important;flex:1;min-width:50px}.anvil-extras-chips-input{display:flex;flex-wrap:wrap;gap:8px;border-bottom:1px solid;align-items:center;padding-bottom:4px}`;

// DesignerPivot.ts
var DesignerPivot = class extends DesignerComponent {
  static init() {
    super.init(".pivot-placeholder");
  }
  constructor(domNode, pyComponent, el) {
    super(domNode, pyComponent, el);
    this.pivot = $(domNode.querySelector(".anvil-extras-pivot"));
  }
  update({rows, columns: cols, values: vals, aggregator: aggregatorName}) {
    const keys = [...rows, ...cols, ...vals, ...["key A", "key B", "key C"]];
    const item = Object.fromEntries(keys.map((key) => [key, 1]));
    this.pivot.pivotUI([item], {rows, cols, vals, aggregatorName}, true);
  }
};
DesignerPivot.links = ["https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.css"];
DesignerPivot.scripts = [
  "https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js",
  "https://cdnjs.cloudflare.com/ajax/libs/pivottable/2.23.0/pivot.min.js"
];
export {
  DesignerChip,
  DesignerChipsInput,
  DesignerComponent,
  DesignerMultiSelectDropDown,
  DesignerPivot,
  DesignerQuill,
  DesignerSlider,
  DesignerSwitch,
  DesignerTabs
};
