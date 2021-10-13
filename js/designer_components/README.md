# Let's create a Designer Component


## Intro

So you want to make a Designer Component that updates dynamically in the Designer?
First - this relies on Javascript.
It also plays around with Skulpt.
It's not officially supported.
It may need updating in the future since it relies on some hackery and implementation details that may change in the future.

BUT it is isolated to the Designer, so if it does stop working - the actual Python code won't be affected.

### Notes
Your custom component must be an HTMLPanel.
We essentially create a Javascript version of our CustomComponent.
Anvil never calls the Python class in the Designer, so that's why we need to inject our Javascript version.
In the Python code, we remove the script tags in the `__init__` method. This way we do not inject the Javascript version into Python.

## Where to start?

Write the Python version first!

When you want to create a Designer version, first look at the comments in `DesignerComponent.ts`.
Anything marked as `private` should NOT be overridden.

- Does your Python class have injected `css`?
  - *override the `static css` property*
- Does your Python class have injected `link` tags?
  - *override the `static links` property*
- Does your Python class have an injected `script` tag?
  - *override the `static script` property*


### `static init()`

You must override the `init()` method and then call `super.init()`

The custom component HTML must have a domNode with an identifiable selector.
e.g.

```html
<div class="quill-editor" style="min-height:150px;"></div>
```

The first argument to `super.init()` should be the selector to identify your custom component in the dom.
```typescript
    static init() {
        super.init(".quill-editor");
    }
```

An optional second argument can be used, which is a className. This className will be added to the HTMLPanel's domNode.
In the Designer world, its purpose is to be a flag to prevent instantiating the same domNode multiple times.
The second argument can be used to add a class to the HTMLPanel you would otherwise have added in your Python `__init__` method.

```typescript
    static init() {
        super.init(".tabs", "anvil-extras-designer");
    }
```


### `constructor(domNode, pyComponent, el)`

A constructor function in javascript is a bit like Python's `__init__` method and `this` acts like `self`.
After the `init` method is called we call the constructor.
There is no need to override the `constructor()` method - but you may want to if you want to add attributes to your `this` argument.
The arguments to the `constructor()` will be:
- the HTMLPanel's domNode for your custom component.
- the Python Component as a Skulpt object.
  (A Skulpt object is what your client-side Python object looks like in Javascript)
- the domNode of the element found from the querySelector used in the `init()` method


### `setProp(propName, propVal, props)`, `update(props, propName, propVal)`

You will need to override `setProp` or `update` (but not both).

In `setProp` you get the `propName` and the `propVal`, as well as all the current `props`.
These are the raw Javascript values.
You can either update the dom directly or work with the Skulpt Python objects.
There are some helper methods for common properties like `visible` and working with `color`.

The `DesignerChips` component is an example that uses `setProp` and works with both Skulpt objects and the dom to update itself when a property changes.

`update` is typically in place of `setProp` when you update your entire component whenever a property changes.
The advantage of `update` is that it is only called once on the first load, whereas `setProp` is called once per prop on the first load.


## Exporting your Designer class
- To make your class available you need to export it in `js/designer_components/index.ts`

## Bundling the javascript
- Install deno
- `cd js/designer_components`
- `deno run -A build-script.ts`
- This will override the bundled files.



## Hacking

In each designer component, you'll see code like

```html
      <script type="module">

      import {DesignerQuill} from "https://deno.land/x/anvil_extras@dev-1.2.1/js/designer_components/bundle.min.js";

      DesignerQuill.init();

      </script>
```

You'll need equivalent code in your custom component's HTML.

When hacking, there's no need to worry about the deno link. Instead:
- bundle the Javascript (see above instructions)
- Copy the bundled file into your theme assets.
- Replace the deno URL with a relative theme URL: `./_/theme/bundle.js`

Whenever you change the local files, re-bundle and repeat.
