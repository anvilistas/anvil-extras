# Let's create a Designer Component


## Intro

So you want to make a Designer Component that updates dynamically in the Desginer?
First - this relies on Javascript.
It also plays around with Skulpt.
It's not officially supported.
It may need updating in the future since it relies on some hackery and implementation details that may change in the future.

BUT it is isolated to the Desiner so if does stop working - the actual python won't be affected.

### Notes
Your custom component must be an HTMLPanel.
We essentially create a Javascript version of our CustomComponent.
Anvil never calls the Python class in the Designer so that's why we need to inject our own Javascript version.
In the Python code we remove the script tags in the `__init__` method so that the Javascript version is never injected.


## Where to start?

Write the python version first!

When you want to create a Designer version look at the comments in `DesignerComponent.ts`.
Anything that is marked as `private` should NOT be overriden.

- Does your Python class have injected `css`?
  - *override the `static css` property*
- Does your Python class have injected `link` tags?
  - *override the `static links` property*
- Does your Python class have an injected `script` tag?
  - *override the `static script` property*


### `static init()`

You must override the `init()` method and then call `super.init()`

The custom component html must have a domNode with an identifiable selector.
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

An optional second argument can be used. Which is a className. This className will be added to the HTMLPanel dom node.
In the Designer world its purpose is to be a flag to prevent instantiating the same domNode multiple times.
But it can be used to add classes to the HTMLPanel you would otherwise have added in your python init method.

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
- the python Component as a Skulpt object.
  (A Skulpt object is what your client side Python object looks like in Javacsript)
- the domNode of the element found from the querySelector used in the `init()` method


### `setProp(propName, propVal, props)`

You will need to override `setProp` or `update` (but not both). It's probably better to override `setProp`.
(`update` was used in the initial versions and `setProp` was later added as a better implementation).
In `setProp` you get the `propName` and the `propVal` as well as all the current `props`.
These are the raw Javascript values.
You can either update the dom directly or work with the Skulpt Python objects.
There are some helper methods for common properties like `visible` and working with `color`.

The DesignerChips component is an example that uses `setProp` and works with both Skulpt objects and the dom to update itself when a property changes.


## Bundling the javascript
Install deno
`cd js/designer_components`
`deno run -A build-script.ts`



## Hacking

In each designer component you'll see code like

```html
      <script type="module">

      import {DesignerQuill} from "https://deno.land/x/anvil_extras@dev-1.2.1/js/designer_components/bundle.min.js";

      DesignerQuill.init();

      </script>
```

You'll need equivalent code in your custom component's html.

When hacking it's probably best to:
- Create a branch
- bundle the javascript (see above instructions)
- push the branch to github
- go to the file of the bundle.js in github and click raw
- grab the url - something like: `https://raw.githubusercontent.com/anvilistas/anvil-extras/main/js/designer_components/bundle.js`
- replace the deno url with this url
