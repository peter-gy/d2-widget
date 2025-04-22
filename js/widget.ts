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
async function diagramToSvg(d2: D2, diagram: string, options: CompileOptions) {
	const result = await d2.compile(diagram, { options, inputPath: "index" });
	return d2.render(result.diagram, { ...result.renderOptions, ...options });
}

export default () => {
	const d2 = new D2();

	return {
		async render({ model, el }: RenderProps<Model>) {
			// Accessors and mutators for the model
			const getDiagram = () => model.get("diagram");
			const getOptions = () => model.get("options");
			const setSvg = (svg: string) => {
				model.set("_svg", svg);
				model.save_changes();
			};

			// Diagramming logic
			const update = async () => {
				try {
					const svg = await diagramToSvg(d2, getDiagram(), getOptions());
					setSvg(svg);
					el.innerHTML = svg;
					el.classList.add("d2-widget");
				} catch (error: unknown) {
					console.error(error);
					const errorMessage =
						error instanceof Error ? error.message : "Unknown error";
					el.innerHTML = `<div class="error">Error generating diagram: ${errorMessage}</div>`;
				}
			};

			// Listeners to re-render diagram on model changes
			model.on("change:diagram", update);
			model.on("change:options", update);

			// Initial render
			await update();
		},
	};
};
