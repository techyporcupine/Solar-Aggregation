// if you plan to use this, change anythign with "TODO:" in the var.
// set this up in appsscript to run every 10 mins (5 mins should also work, just don't get ratelimited...)

function slideTest() {
  let presentation = SlidesApp.openById('TODO:ID_OF_SLIDESHOW');
  const slide = presentation.getSlides()[0]; // get slide 0
  const images = slide.getImages(); // image array

  Logger.log("Images found: " + images.length);
  const newImageURL = 'TODO:FULL_URL_OF_IMAGE_HERE' // image to replace with
  images.forEach(image => {
    // see which image has "REPLACE" in alt text title
    if (image.getTitle() === 'REPLACE') {
      image.replace(newImageURL, true); // replace image, and crop it (the true does that)
      image.setTitle('REPLACE')
    }
  });
}
