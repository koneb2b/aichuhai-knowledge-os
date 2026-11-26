import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        base: "#07090A",
        surface: "#0C0F11",
        raised: "#12161A",
        line: "rgba(255,255,255,0.07)",
        "line-strong": "rgba(255,255,255,0.14)",
        ink: "#ECEEF0",
        dim: "#A3ABB1",
        faint: "#767F86",
        accent: "#D9A05B",
        pass: "#5BD6A0",
        fail: "#F07178",
      },
      fontFamily: {
        sans: [
          "ui-sans-serif",
          "system-ui",
          "-apple-system",
          "Segoe UI",
          "Microsoft YaHei",
          "PingFang SC",
          "sans-serif",
        ],
        mono: [
          "ui-monospace",
          "SFMono-Regular",
          "Menlo",
          "Consolas",
          "monospace",
        ],
        serif: [
          "Iowan Old Style",
          "Palatino Linotype",
          "Book Antiqua",
          "Georgia",
          "Times New Roman",
          "serif",
        ],
      },
      borderRadius: {
        DEFAULT: "3px",
        sm: "2px",
        md: "4px",
        lg: "6px",
      },
    },
  },
  plugins: [],
};

export default config;
