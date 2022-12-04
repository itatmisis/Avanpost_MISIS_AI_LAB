const BACKEND_API = 'http://localhost:5002'//http://158.160.32.20:8000'
const IMAGES_URL = 'http://158.160.32.20:8001/datasets/default'


$(function () {
  const form = document.querySelector(".form1"),
    fileInput = document.querySelector(".file-input"),
    form2 = document.querySelector(".form2"),
    fileInput2 = document.querySelector(".file-input-2")

  $(document).ready(function () {

    form.addEventListener("click", () => {
      fileInput.click();
    });

    form2.addEventListener("click", () => {
      fileInput2.click();
    });

    window.console = window.console || function (t) { };


    if (document.location.search.match(/type=embed/gi)) {
      window.parent.postMessage("resize", "*");
    }

    const hamBtn = document.querySelector(".ham-btn");
    const nav = document.querySelector(".nav");

    hamBtn.addEventListener("click", () => {
      nav.classList.toggle("dis");
      document.body.classList.toggle("overflow");
    });
    const day = document.querySelector(".day");

    day.addEventListener("click", () => {
      document.body.classList.toggle("dark");
      day.style.display = "none";
      night.style.display = "block";
    });
    const night = document.querySelector(".night");

    night.addEventListener("click", () => {
      document.body.classList.toggle("dark");
      night.style.display = "none";
      day.style.display = "block";
    });

    $("#predict-btn").on('click', () => {
      predict();
    })

    const preloader = document.querySelector(".pre-loader");

    window.addEventListener("load", () => (preloader.style.display = "none"));


    const conbtn = document.querySelector(".conbtn");
    const navBtn1 = document.querySelector(".nav-btn1");
    const navBtn2 = document.querySelector(".nav-btn2");
    const navBtn3 = document.querySelector(".nav-btn3");
    const navBtn4 = document.querySelector(".nav-btn4");
    const navBtn5 = document.querySelector(".nav-btn5");

    const about = document.querySelector(".row");
    const skills = document.querySelector(".skills");
    const portfolio = document.querySelector(".portfolios");
    const services = document.querySelector(".services");
    const contact = document.querySelector(".contact");

    navBtn2.addEventListener('click', () => {
      portfolio.classList.remove("sec-dis")
      about.classList.remove("sec-dis")
      services.classList.remove("sec-dis")

      contact.classList.remove("sec-dis")

      navBtn5.classList.remove("active")

      navBtn1.classList.remove("active")
      navBtn3.classList.remove("active")
      navBtn4.classList.remove("active")

      navBtn2.classList.add("active")
      skills.classList.add("sec-dis")
      nav.classList.toggle("dis");
      document.body.classList.toggle("overflow");

    })
    navBtn1.addEventListener('click', () => {
      portfolio.classList.remove("sec-dis")
      about.classList.add("sec-dis")
      navBtn1.classList.add("active")
      navBtn3.classList.remove("active")
      navBtn4.classList.remove("active")
      contact.classList.remove("sec-dis")

      navBtn5.classList.remove("active")
      services.classList.remove("sec-dis")
      navBtn2.classList.remove("active")
      skills.classList.remove("sec-dis")
      nav.classList.toggle("dis");
      document.body.classList.toggle("overflow");

    })
    navBtn3.addEventListener('click', () => {
      portfolio.classList.add("sec-dis")
      about.classList.remove("sec-dis")
      navBtn1.classList.remove("active")
      navBtn3.classList.add("active")
      navBtn4.classList.remove("active")
      contact.classList.remove("sec-dis")

      navBtn5.classList.remove("active")
      services.classList.remove("sec-dis")
      navBtn2.classList.remove("active")
      skills.classList.remove("sec-dis")
      nav.classList.toggle("dis");
      document.body.classList.toggle("overflow");

    })
    navBtn4.addEventListener('click', () => {
      portfolio.classList.remove("sec-dis")
      about.classList.remove("sec-dis")
      navBtn1.classList.remove("active")
      navBtn3.classList.remove("active")
      navBtn4.classList.add("active")
      contact.classList.remove("sec-dis")

      navBtn5.classList.remove("active")
      services.classList.add("sec-dis")
      navBtn2.classList.remove("active")
      skills.classList.remove("sec-dis")
      nav.classList.toggle("dis");
      document.body.classList.toggle("overflow");

    })
    navBtn5.addEventListener('click', () => {
      portfolio.classList.remove("sec-dis")
      about.classList.remove("sec-dis")
      navBtn1.classList.remove("active")
      navBtn3.classList.remove("active")
      navBtn4.classList.remove("active")
      contact.classList.add("sec-dis")

      navBtn5.classList.add("active")
      services.classList.remove("sec-dis")
      navBtn2.classList.remove("active")
      skills.classList.remove("sec-dis")
      nav.classList.toggle("dis");
      document.body.classList.toggle("overflow");

    })

    $(".add-class").on('click', () => {
      let className = $('#class-name').val();
      let isAddParser = $('#is-use-parser').is(":checked");
      let parserCount = $('#parser-count').val();

    });

    $('#class-name').on('input',
      function
        (e) {
        $("#btn-add-class").prop("disabled", !isAddClassBtnEnabled())
      });

    $('#parser-count').on('input',
      function
        (e) {
        $("#btn-add-class").prop("disabled", !isAddClassBtnEnabled())
      });

    $("#btn-add-class").on('click', () => {
      uploadFile();
    });

    fileInput.onchange = function (e) {
      $(".count-images").text(`Выбрано ${form[0].files.length} изображения(-ий)`)
    };


    function uploadFile() {
      let xhr = new XMLHttpRequest();
      xhr.open("POST", `${BACKEND_API}/UploadImages`);

      let data = new FormData();
      console.log(form[0].files);

      let totalSize = 0;
      $.each(form[0].files, function (i, file) {
        data.append('file', file);
        totalSize += file.size;
      });
      const className = document.querySelector(".form-control")
      data.append("request", JSON.stringify({
        ClassName: className.value
      }))

      xhr.upload.onprogress = ({
        loaded,
        total
      }) => {
        let fileLoaded = Math.floor((loaded / totalSize) * 100);
        console.log(fileLoaded)
        changeProgressBarValue(fileLoaded)
        //uploadedArea.classList.add("onprogress");
        if (loaded == total) {
          ToTrainTable();
        }
      }


      xhr.send(data);

      xhr.onload = function () {
        Swal.fire({
          position: 'top-end',
          icon: 'success',
          title: 'Класс успешно создан',
          showConfirmButton: false,
          timer: 1500
        })
        afterSave();
      };

      xhr.onerror = function () {
        Swal.fire({
          icon: 'error',
          title: 'Oops...',
          text: 'Something went wrong!',
          footer: '<a href="">Про создании класса произошла оишбка :((</a>'
        })
        afterSave();
      };
    }
  })


  function predict() {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", `${BACKEND_API}/Predict`);

    let data = new FormData();
    console.log(form2[0].files);

    let totalSize = 0;
    $.each(form2[0].files, function (i, file) {
      data.append('file', file);
      totalSize += file.size;
    });
    const className = document.querySelector(".form-control")
    xhr.upload.onprogress = ({
      loaded,
      total
    }) => {
      let fileLoaded = Math.floor((loaded / totalSize) * 100);
      console.log(fileLoaded)
      changeProgressBarValue(fileLoaded)
      //uploadedArea.classList.add("onprogress");
      if (loaded == total) {
        ToTrainTable();
      }
    }

    function checkData() {
      console.log(xhr.readyState);
    }

    xhr.onreadystatechange = checkData;
    xhr.send(data);
  }




  function isAddClassBtnEnabled() {
    let className = $('#class-name').val();
    let isAddParser = $('#is-use-parser').is(":checked");
    let parserCount = $('#parser-count').val();

    return className.length > 0 || (isAddParser && parserCount > 0)
  }

  function afterSave() {
    $('#class-name').val("");
    $('#is-use-parser').prop('checked', false)
    $('#parser-count').val(0);
    $(".count-images").text();
    $("#class-name").val('');
  }

  function parseImages(name) {

    const preloader = document.querySelector(".pre-loader");
    preloader.style.display = 'inherit';
    $.ajax({
      url: `${BACKEND_API}Parser/Parse`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      method: 'POST',
      dataType: 'json',
      data: JSON.stringify({ ClassName: name }),
      success: function (data) {
        console.log(data)
        console.log(data.length)
        var count = 10;
        if (data.length < 10) {
          count = data.length;
        }

        var block = $("#parsed-images");

        for (let i = 0; i < count; i++) {
          block.append(`<a>${IMAGES_URL}/${name}/${data[i]}</a> <br> `)
        }
        preloader.style.display = 'none';
      },
      error: function (error) {
        preloader.style.display = 'none';
        console.log(error)
      }
    });
  }

  $("#show-parse-example").on('click', () => {
    let className = $('#class-name').val();
    parseImages(className)
  })

  function run_waitMe(effect) {
    $('#parsed-wait').waitMe({

      //none, rotateplane, stretch, orbit, roundBounce, win8, 
      //win8_linear, ios, facebook, rotation, timer, pulse, 
      //progressBar, bouncePulse or img
      effect: 'bounce',

      //place text under the effect (string).
      text: '',

      //background for container (string).
      bg: 'rgba(255,255,255,0.7)',

      //color for background animation and text (string).
      color: '#000',

      //max size
      maxSize: '',

      //wait time im ms to close
      waitTime: -1,

      //url to image
      source: '',

      //or 'horizontal'
      textPos: 'vertical',

      //font size
      fontSize: '',

      // callback
      onClose: function () { }

    });
  }

})


