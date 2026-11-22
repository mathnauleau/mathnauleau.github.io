const fs = require("node:fs");
const path = require("node:path");

const source = require.resolve("@mathieu.nauleau/tokens/css");
const destination = path.join(__dirname, "tokens.css");

const header =
  "/* Generated from @mathieu.nauleau/tokens — do not edit. Run `npm run sync-tokens`. */\n";

fs.writeFileSync(destination, header + fs.readFileSync(source, "utf8"));
console.log("Synced design tokens to tokens.css");
