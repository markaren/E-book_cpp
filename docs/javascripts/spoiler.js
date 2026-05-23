// Reveal a blurred solution when it is clicked.
// Combined with the collapsible "Show solution" block, this means a reader
// needs two deliberate clicks before the answer is visible: one to expand
// the block, and one to un-blur the solution inside it.
//
// A single delegated listener on `document` survives Material's instant
// navigation, so it does not need re-binding on every page load.
document.addEventListener("click", function (e) {
  const spoiler = e.target.closest(".spoiler");
  if (spoiler) {
    spoiler.classList.add("spoiler--revealed");
  }
});
