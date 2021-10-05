import { DesignerComponent } from "./DesignerComponent.ts";

declare var Quill: any;
export class DesignerQuill extends DesignerComponent {
    static defaults = {
        auto_expand: true,
        content: "",
        height: 150,
        placeholder: null,
        readonly: false,
        theme: "snow",
        toolbar: true,
        visible: true,
    };
    static links = ["//cdn.quilljs.com/1.3.6/quill.snow.css", "//cdn.quilljs.com/1.3.6/quill.bubble.css"];
    static scripts = ["//cdn.quilljs.com/1.3.6/quill.min.js"];

    static init() {
        super.init(".quill-editor");
    }
    editor: HTMLElement;
    constructor(domNode: HTMLElement, pyComponent: any, editor: HTMLElement) {
        super(domNode, pyComponent, editor);
        this.editor = editor;
    }
    update(props: any): void {
        if (this.editor.firstElementChild) {
            this.editor.removeChild(this.editor.firstElementChild); // remove the editor and the toolabar
        }
        if (this.domNode.firstElementChild !== this.editor) {
            this.domNode.removeChild(this.domNode.firstElementChild); // remove the toolbar
        }
        const q = new Quill(this.editor, {
            modules: { toolbar: props.toolbar || false },
            readOnly: props.readonly,
            theme: props.theme,
            placeholder: props.placeholder,
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
}
