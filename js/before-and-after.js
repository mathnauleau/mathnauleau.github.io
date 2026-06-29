// get the div containing both the before and after images
const imageWrapper = document.querySelector(`.before-after-wrapper`);
// check if the user is using a touch device
const isTouch = window.matchMedia("(pointer: coarse)").matches;

// initialize the dragElement function below
dragElement(imageWrapper.querySelector(".handle"));

// get the current coordinates of the .handle
function getCoords(e) {
  let x, y;

  // get the current x and y of the users input (dragging .handle)
  // check if the device is a touch device
  if (isTouch) {
    // touchscreen: if the devices is a touch device, the x and y will be in the touches[0] object
    x = e.touches[0].clientX;
    y = e.touches[0].clientY;
  } else {
    //
    // desktop: if the device is not a touch device we can get it right from the event (e) object
    x = e.clientX;
    y = e.clientY;
  }

  return { x, y };
}

// listens for the user touch/mouse input on the .handle element and drags the slider
function dragElement(el) {
  let pos1 = 0,
    pos2 = 0,
    pos3 = 0,
    pos4 = 0;

  // initialize the slider being dragged when the .handle is pressed
  if (isTouch) {
    el.ontouchstart = dragInit;
  } else {
    el.onmousedown = dragInit;
  }

  // call elementDrag/closeElementDrag when the users interacts with .handle
  function dragInit(e) {
    e = e || window.event;
    e.preventDefault();

    // get the mouse cursor/touch position at startup
    const { x, y } = getCoords(e);
    pos3 = x;
    pos4 = y;

    if (isTouch) {
      document.ontouchend = closeElementDrag; // stop moving
      document.ontouchmove = elementDrag; // call function whenever the cursor moves
    } else {
      document.onmouseup = closeElementDrag; // stop moving
      document.onmousemove = elementDrag; // call function whenever the cursor moves
    }
  }

  // as the element is dragged update the .before-image-wrapper width
  function elementDrag(e) {
    e = e || window.event;
    e.preventDefault();

    // calculate new cursor position:
    const { x, y } = getCoords(e);
    pos1 = pos3 - x;
    pos2 = pos4 - y;
    pos3 = x;
    pos4 = y;

    let wrapperRight = el.offsetLeft - pos1;

    if (wrapperRight >= 0 && wrapperRight <= imageWrapper.offsetWidth) {
      // set the element's new position:
      el.style.left = `${el.offsetLeft - pos1}px`;
      imageWrapper.querySelector(".before-image-wrapper").style.width =
        `${wrapperRight}px`;
    }
  }

  function closeElementDrag() {
    if (isTouch) {
      document.ontouchend = null;
      document.ontouchmove = null;
    } else {
      document.onmouseup = null;
      document.onmousemove = null;
    }
  }
}
