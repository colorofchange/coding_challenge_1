import uglify from "gulp-uglify";
import { src, dest, parallel } from "gulp";
import image from "gulp-image";

export const minifyJS = () => src("./static/js/public/*.js")
  .pipe(uglify())
  .pipe(dest("./static/js/public/"));

export const minifyImages = () => src("static/images/**/*.png").pipe(image()).pipe(dest("static/images/"));

export const minifyCSS = () => src("./static/scss/main.css", { allowEmpty: true } )
  .pipe(uglify())
  .pipe(dest("./static/scss/"));

export const prod = parallel(minifyImages, minifyJS, minifyCSS);

export const staging = prod;

export default (done) => {
  minifyImages();
  done();
};
