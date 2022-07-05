let files = [];
let dataTransfer = new DataTransfer();
const imgpreviewlist = document.querySelector(".img-preview-list");
const fileDropBox = document.querySelector("#fileDropBox");
const input = document.querySelector("#id_all_large_images");

if (input) {
  input.addEventListener("change", (e) => {
    let file = input.files;

    for (let i = 0; i < file.length; i++) {
      files.push(file[i]);
      dataTransfer.items.add(file[i]);
    }
    showImages();
  });
}

const showImages = () => {
  let images = "";

  files.forEach((value, index) => {
    const currentSRC = URL.createObjectURL(value);
    images += ` <div class="img-preview-div">
        <img
          class="img-preview"
          src="${currentSRC}"
          alt=""
        />
        <span
        onClick="delImg(${index})"
          class="fs-4"
          style="
            height: fit-content;
            color: red;
            background: #ebebeb;
            padding-left: 10px;
            padding-right: 10px;
            padding-bottom: 7px;
            border-radius: 4px;
            margin-left: 42px;
          "
          >×</span
        >
      </div>`;
  });

  imgpreviewlist.innerHTML = images;
};

const delImg = (index) => {
  files.splice(index, 1);
  dataTransfer.items.remove(index);
  input.files = dataTransfer.files;

  showImages();
};
