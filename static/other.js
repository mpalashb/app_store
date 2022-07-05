const messageID = document.querySelectorAll("#message-block");
const timeout = 5000;

const removeMsgORDisplay = (time, querySel) => {
  const query = querySel[0];
  setTimeout(() => {
    if (query) {
      query.style.display = "none";
    }
  }, time);
};

const id_thumb_img = document.getElementById("id_thumb_img");
const prevthumbid = document.getElementById("prev-thumb-id");

if (id_thumb_img) {
  id_thumb_img.addEventListener("change", () => {
    const getCurrThumbSRC = URL.createObjectURL(id_thumb_img.files[0]);
    prevthumbid.innerHTML = `<div
              class="prev-thumb"
              style="
                display: flex;
                justify-content: center;
                margin-bottom: 50px;
              "
            >
  <img
  class="prev-thumb-img"
  src="${getCurrThumbSRC}"
  alt=""
  style="max-width: 120px; border-radius: 5px"
/>
</div>
`;
  });
}

const removeUploadThumb = (e) => {
  // console.log("clicked");
  e.preventDefault();
  id_thumb_img.value = "";
  prevthumbid.innerHTML = "";
};

const getUploadThumb = document.querySelector("#id_thumb_img");
if (getUploadThumb) {
  const getUploadThumb2 = getUploadThumb.nextElementSibling.nextElementSibling;
  if (getUploadThumb2) {
    getUploadThumb2.addEventListener("click", removeUploadThumb, false);
  }
}

removeMsgORDisplay(timeout, messageID);

if (getUploadThumb) {
  getUploadThumb.nextElementSibling.addEventListener(
    "click",
    () => info(),
    false
  );
}

const info = () => {
  prevthumbid.previousElementSibling.innerHTML = `<div class="alert alert-info mb-5" role="alert">
  Upload is default!
</div>`;
  setTimeout(() => {
    prevthumbid.previousElementSibling.innerHTML = "";
  }, 3000);
};

const id_category = document.getElementById("id_category");
if (id_category) {
  id_category.required = false;
}

if (document.getElementById("id_category")) {
  document.getElementById("id_category").required = false;
}

if (document.getElementById("id_name")) {
  document.getElementById("id_name").required = false;
}
