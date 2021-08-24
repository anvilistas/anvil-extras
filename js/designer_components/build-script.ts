import * as esbuild from "https://deno.land/x/esbuild@v0.11.10/mod.js";
// import * as esbuild from "esbuild";
// deno run -A build-script.ts

let result = await esbuild.build({
    entryPoints: ["index.ts"],
    bundle: true,
    format: "esm",
    outfile: "bundle.min.js",
    minify: true,
});

console.log("result:", result);

result = await esbuild.build({
    entryPoints: ["index.ts"],
    bundle: true,
    format: "esm",
    outfile: "bundle.js",
});

console.log("result:", result);
esbuild.stop();
