/**
 * Import D2 from CDN instead of bundling it to:
 * 1. Keep the anywidget bundle size small
 * 2. Work around notebook environment display limits in WASM environments
 *    (e.g., Marimo's OUTPUT_MAX_BYTES: https://github.com/marimo-team/marimo/issues/3376)
 */

import type { RenderProps } from "@anywidget/types";
import { type CompileOptions, D2 } from "https://esm.sh/@terrastruct/d2@0.1.23";
import "./widget.css";

/* Specifies attributes defined with traitlets in ../src/d2_widget/__init__.py */
interface Model {
	_svg: string;
	diagram: string;
	options: CompileOptions;
}

// TODO(peter-gy): Consider adding support for accepting `CompileRequest` payload with `fs` map allowing resolution of .d2 files referenced and imported in diagrams.
// See: https://d2lang.com/tour/imports

const DEFAULT_INPUT_PATH = "index";

async function diagramToSvg(d2: D2, diagram: string, options: CompileOptions) {
	// For now we only support single-file diagrams
	const result = await d2.compile(diagram, {
		options,
		inputPath: DEFAULT_INPUT_PATH,
	});
	const renderedSvg = await d2.render(result.diagram, {
		...result.renderOptions,
		...options,
	});
	return renderedSvg;
}

export default () => {
	const d2 = new D2();
	let isRendering = false;

	return {
		async render({ model, el }: RenderProps<Model>) {
			// Accessors and mutators for the model
			const getDiagram = () => model.get("diagram");
			const getOptions = () => model.get("options");
			const setSvg = (svg: string) => {
				model.set("_svg", svg);
				model.save_changes();
			};
			const getRoot = () => {
				const root = el.firstChild as HTMLElement;
				if (!root) {
					throw new Error("Root element not found");
				}
				return root;
			};

			// Diagramming logic
			const update = async () => {
				// If another update is already in progress, do nothing
				if (isRendering) {
					console.log("Another update is already in progress, skipping");
					return;
				}

				isRendering = true;
				try {
					const svg = await diagramToSvg(d2, getDiagram(), getOptions());
					setSvg(svg);
					getRoot().innerHTML = svg;
				} catch (error: unknown) {
					console.error(error);
					const errorMessage =
						error instanceof Error ? error.message : "Unknown error";
					getRoot().innerHTML = `<div class="error">Error generating diagram: ${errorMessage}</div>`;
				}
				isRendering = false;
			};

			// Set up root element
			const root = document.createElement("div");
			el.appendChild(root);
			el.classList.add("d2-widget");

			// Listeners to re-render diagram on model changes
			model.on("change:diagram", update);
			model.on("change:options", update);

			// Initial render
			await update();
		},
	};
};
