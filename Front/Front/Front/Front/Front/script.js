const BACKEND_API = 'http://51.250.88.247:8000' //http://158.160.32.20:8000''http://localhost:5002'
const IMAGES_URL = 'http://51.250.88.247:8001/images/'
var classes = []
var classs = []
$(function () {
    const form = document.querySelector(".form1"),
        fileInput = document.querySelector(".file-input")
    getClassesToTrain()

    $(document).ready(function () {
        ToAddClass();
        // const startingIntent = 'Модель';
        // const mergedStory = {'Модель': 'версия 1'}
        // createGraph(startingIntent, mergedStory[startingIntent])
        fileInput.onchange = function (e) {
                $(".count-images").text(`Выбрано ${form[0].files.length} изображения(-ий)`)
                
            };

        form.addEventListener("click", () => {
            fileInput.click();
        });

        $(document).on('click',
            '.add-class-btn',
            function () {
                showProgressBar();
                uploadFile();
                hideProgressBar();
                
            });


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
                    //location.reload()
                    setTToTrainTable()
                }
            }


            xhr.send(data);
        }

        // xhr.onload = function () {
        //     Swal.fire({
        //       position: 'top-end',
        //       icon: 'success',
        //       title: 'Класс успешно создан',
        //       showConfirmButton: false,
        //       timer: 1500
        //     })
        //     afterSave();
        //   };
    
        //   xhr.onerror = function () {
        //     Swal.fire({
        //       icon: 'error',
        //       title: 'Oops...',
        //       text: 'Something went wrong!',
        //       footer: '<a href="">Про создании класса произошла оишбка :((</a>'
        //     })
        //     afterSave();
        //   };
        
        $(document).on('click',
        '.parser-example',
        function () {
            console.log()
            parseImages(document.querySelector(".form-control").value)
            // $('.add-class-btn').prop('disabled', true);
        })

          function parseImages(name) {
            console.log(name)
            
            // const preloader = document.querySelector(".pre-loader");
            // preloader.style.display = 'inherit';
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
                // preloader.style.display = 'none';
                console.log(error)
              }
            });
          }
        
        
    });

    $(document).on('click',
        '.to-add-class',
        function () {
            ToAddClass();
            // $('.add-class-btn').prop('disabled', true);
        })

    $(document).on('click',
        '.zero-models-button',
        function () {
            ToAddClass();
        })

    $(document).on('click',
        '.to-train',
        function () {
            ToTrainTable();
        })

    $(document).on('click',
        '.to-model-version',
        function () {
            ToVersionHistoryTable();
        })

    $(document).on('click',
        '.to-test-model',
        function () {
            ToModelTestTable();
        })

    $(document).on('change',
        '.file-input',
        function () {
            if (document.querySelector(".form-control").value != '') {
                $('.add-class-btn').prop('disabled', false);
            }
        });

    $('#parser').click(function () {
        if ($(this).is(':checked')) {
            $('.image-number').show(100);
        } else {
            $('.image-number').hide(100);
        }
       
        // if (document.querySelector(".form-control").value!='')  { $(".parser-example").prop('disabled', 'false')}
        //     else {$(".parser-example").prop('disabled', 'true')}
          
    });

    $('.number-control').on('change', function () {
        console.log(parseInt(document.querySelector(".number-control").value))
        if (parseInt(document.querySelector(".number-control").value) > 0) {
            $('.add-class-btn').prop('disabled', false);
        }
        else {
            $('.add-class-btn').prop('disabled', true);
        }
    });

    $(document).ready(function () {
        $('.add-class-btn').prop('disabled', true);
        $('.image-number').hide();
        const output = [];

        const input =  [
            {
                "id": 1,
                "parent_id": 1,
                "name": "1111",
                "images": [
                    "1111/1.png"
                ]
            },
            {
                "id": 2,
                "parent_id": 1,
                "name": "1111",
                "images": [
                    "1111/img_03.jpg",
                    "1111/img_02.jpg",
                    "1111/img_01.jpg"
                ]
            },
            {
                "id": 3,
                "parent_id": 1,
                "name": "dogs",
                "images": [
                    "dogs/DVzW3t1zjZg.png"
                ]
            },
            {
                "id": 4,
                "parent_id": 1,
                "name": "cars",
                "images": [
                    "cars/img_03.jpg",
                    "cars/img_02.jpg",
                    "cars/img_01.jpg"
                ]
            },
            {
                "id": 5,
                "parent_id": 4,
                "name": "andrey",
                "images": [
                    "andrey/J3FW7g0dBB0.jpg",
                    "andrey/UEtWsMld998.jpg",
                    "andrey/Xcs6LvQ6MLk.png"
                ]
            },
            {
                "id": 6,
                "parent_id": 1,
                "name": "1111",
                "images": [
                    "1111/1.png"
                ]
            },
            {
                "id": 7,
                "parent_id": 4,
                "name": "books",
                "images": [
                    "books/515VbB52deL._AC_SY780_.jpg",
                    "books/978-1-4613-8476-2.jpeg"
                ]
            },
            {
                "id": 8,
                "parent_id": 1,
                "name": "1111",
                "images": []
            }
        ]

for (const item of input) {
  output[item.id - 1] = item;
}
for (const item of output) {
    // console.log(item)
  if (item.id !== item.parent_id) {
    const parent = output[item.parent_id - 1];
    if (!Array.isArray(parent.children)) {
      parent.children = [];
    }
    parent.children.push(item);
  }
}
// console.log(Object.entries(output[0]));

        output.forEach(function (item) {
            // console.log(item.parent_id)
            var parent = document.querySelector('.parent')
            // console.log(parent.querySelector(`[id='${item.parent_id}']`))
            if( parent.querySelector(`[id='${item.parent_id}']`))
            {
                var ul = document.createElement('ul');
            var li = document.createElement('li');
            var span = document.createElement('span');
            span.innerHTML = `Версия ${item.id} класс ${item.name}`;
            li.classList.add('parent')
            li.id = `${item.id}`
            ul.appendChild(li)
            li.appendChild(span)
            parent.querySelector(`[id='${item.parent_id}']`).appendChild(li);
        }
            else 
            {   var ul = document.createElement('ul');
                var li = document.createElement('li');
                var span = document.createElement('span');
                span.innerHTML = `Версия ${item.id} класс ${item.name}`;
                ul.classList.add('parent')
                ul.id = `${item.id}`
                ul.appendChild(li)
                li.appendChild(span)
                parent.appendChild(ul);
            }
            });
    });
})


function ToAddClass() {
    $(".body-add-class").css("display", "inherit");
    $(".body-train").css("display", "none");
    $(".body-version-history").css("display", "none");
    $(".body-model-test").css("display", "none");
    $(".to-add-class").css({"padding-bottom": "8px",
    "border-bottom": "2px solid #8BFBFF"});
    $(".to-train").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
    $(".to-model-version").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
    $(".to-test-model").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
}

function ToTrainTable() {
    $(".body-add-class").css("display", "none");
    $(".body-train").css("display", "inherit");
    $(".body-version-history").css("display", "none");
    $(".body-model-test").css("display", "none");
    $(".to-add-class").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
    $(".to-train").css({"padding-bottom": "8px",
    "border-bottom": "2px solid #8BFBFF"});
    $(".to-model-version").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
    $(".to-test-model").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
}

function ToVersionHistoryTable() {
    $(".body-add-class").css("display", "none");
    $(".body-train").css("display", "none");
    $(".body-version-history").css("display", "inherit");
    $(".body-model-test").css("display", "none");
    $(".to-add-class").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
    $(".to-train").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
    $(".to-model-version").css({"padding-bottom": "8px",
    "border-bottom": "2px solid #8BFBFF"});
    $(".to-test-model").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
}

function ToModelTestTable() {
    $(".body-add-class").css("display", "none");
    $(".body-train").css("display", "none");
    $(".body-version-history").css("display", "none");
    $(".body-model-test").css("display", "inherit");
    $(".to-add-class").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
    $(".to-train").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
    $(".to-model-version").css({"padding-bottom": "8px",
    "border-bottom": "0px "});
    $(".to-test-model").css({"padding-bottom": "8px",
    "border-bottom": "2px solid #8BFBFF"});
    $(".test-prediction").css("display", "inherit");
    $(".prediction").css("display", "none");
}


function showProgressBar() {
    $(".progress-bar").css("visibility", "visible");
}

function hideProgressBar() {
    $(".progress-bar").css("visibility", "hidden");
}

function changeProgressBarValue(percents) {
    $(".progress-bar").html(`${percents}%`);
    $(".progress-bar").css('width', `${percents}%`)
}

function getClassesToTrain() {
    console.log(BACKEND_API)
    $.ajax({
        url: `${BACKEND_API}/DataClasses/AllClasses`,
        method: 'get',
        dataType: 'json',
        
        success: function (data) {
            console.log('success')
            
            if (data.length != 0){
            $(".zero-models").css("display", "none");
            $(".choose-models").css("display", "inherit");}
            else {
                $(".zero-models").css("display", "inherit");
            $(".choose-models").css("display", "none");
            }
            // build the gallery
            showClassesData(data)
            // data = Object.entries(data)
           
            data.map((i) => {
               console.log(i.images.length != 0 ? `${IMAGES_URL}${i.images[0]}` : 'berlin1.jpg')  
            classes.push({ //
                src:   i.images.length != 0 ? `${IMAGES_URL}${i.images[0]}` : 'berlin1.jpg',     // image url
                srct:  i.images.length != 0 ? `${IMAGES_URL}${i.images[0]}` : 'berlin1t.jpg',    // thumbnail url
                title: i.name         // element title
              })}
               )
            console.log(data, classes, classs)


            $("#my_nanogallery2").nanogallery2({
                thumbnailSelectable :   true,   // enables selection mode
                items: 
                classes,
                // [
                //   {
                //     src:   'berlin1.jpg',     // image url
                //     srct:  'berlin1t.jpg',    // thumbnail url
                //     title: "Berlin"         // element title
                //   },
                //   { src: 'berlin2.jpg', srct: 'berlin2t.jpg', title: 'Cars' },
                //   { src: 'berlin3.jpg', srct: 'berlin3t.jpg', title: 'Skateboards' }
                // ],
                thumbnailWidth:         'auto',
                thumbnailHeight:        '200px',
                itemsBaseURL: 'https://nanogallery2.nanostudio.org/samples/',
                thumbnailHoverEffect2: null,
                locationHash: false
              })
             
              $(".nGY2Gallery").css({"width": "1000px", "height": "70vh", "overflow": "scroll"})
            //   $("#my_nanogallery2").css({})
            
            // retrieve selected items
            $("#my_nanogallery2").on( 'itemSelected.nanogallery2 itemUnSelected.nanogallery2', function() {
              var ngy2data = $("#my_nanogallery2").nanogallery2('data');
              
              // counter 
              $('#nb_selected').text(ngy2data.gallery.nbSelected);
              
              // selected items
              var sel = '';
              ngy2data.items.forEach( function(item) {
                if( item.selected ) {
                  sel += item.GetID() + '[' + item.title + '] ';
                }
              });
              $('#selection').text(sel);
            });
        },
        error: function (error) {
            console.log(error)
            $(".zero-models").css("display", "inherit");
            $(".choose-models").css("display", "none");
        }
    });
}

function showClassesData(data) {
    console.log(data)
}

$(document).ready(function () {
    const form2 = document.querySelector(".form2"),
        fileInput2 = document.querySelector(".file-input-2")
        console.log(form2, fileInput2)
    $(document).on('click',
    '.btn-test',
    function () {
        predict()
    });

    form2.addEventListener("click", () => {
        fileInput2.click();
    });

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
        console.log(data)
        // fileInput.onchange = function (e) {
        //     $(".count-images").text(`Выбрано ${form[0].files.length} изображения(-ий)`)
        // };

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
            // ToTrainTable();
            $(".test-prediction").css("display", "none");
        $(".prediction").css("display", "inherit");
        $(".card__image_current").value = form2[0].files[0]
          }
        }
    
        function checkData() {
          console.log(xhr.response);
        }
    
        xhr.onreadystatechange = checkData;
        xhr.send(data);
      }


    $(document).on('click',
    '.btn-again',
    function () {
        $(".test-prediction").css("display", "inherit");
        $(".prediction").css("display", "none");
    });
    
  const { gsap, imagesLoaded } = window;

const buttons = {
	prev: document.querySelector(".btn--left"),
	next: document.querySelector(".btn--right"),
};
const cardsContainerEl = document.querySelector(".cards__wrapper");
const appBgContainerEl = document.querySelector(".app__bg");

const cardInfosContainerEl = document.querySelector(".info__wrapper");

buttons.next.addEventListener("click", () => swapCards("right"));

buttons.prev.addEventListener("click", () => swapCards("left"));

function swapCards(direction) {
	const currentCardEl = cardsContainerEl.querySelector(".current--card");
	const previousCardEl = cardsContainerEl.querySelector(".previous--card");
	const nextCardEl = cardsContainerEl.querySelector(".next--card");

	const currentBgImageEl = appBgContainerEl.querySelector(".current--image");
	const previousBgImageEl = appBgContainerEl.querySelector(".previous--image");
	const nextBgImageEl = appBgContainerEl.querySelector(".next--image");

	changeInfo(direction);
	swapCardsClass();

	removeCardEvents(currentCardEl);

	function swapCardsClass() {
		currentCardEl.classList.remove("current--card");
		previousCardEl.classList.remove("previous--card");
		nextCardEl.classList.remove("next--card");

		currentBgImageEl.classList.remove("current--image");
		previousBgImageEl.classList.remove("previous--image");
		nextBgImageEl.classList.remove("next--image");

		currentCardEl.style.zIndex = "50";
		currentBgImageEl.style.zIndex = "-2";

		if (direction === "right") {
			previousCardEl.style.zIndex = "20";
			nextCardEl.style.zIndex = "30";

			nextBgImageEl.style.zIndex = "-1";

			currentCardEl.classList.add("previous--card");
			previousCardEl.classList.add("next--card");
			nextCardEl.classList.add("current--card");

			currentBgImageEl.classList.add("previous--image");
			previousBgImageEl.classList.add("next--image");
			nextBgImageEl.classList.add("current--image");
		} else if (direction === "left") {
			previousCardEl.style.zIndex = "30";
			nextCardEl.style.zIndex = "20";

			previousBgImageEl.style.zIndex = "-1";

			currentCardEl.classList.add("next--card");
			previousCardEl.classList.add("current--card");
			nextCardEl.classList.add("previous--card");

			currentBgImageEl.classList.add("next--image");
			previousBgImageEl.classList.add("current--image");
			nextBgImageEl.classList.add("previous--image");
		}
	}
}

function changeInfo(direction) {
	let currentInfoEl = cardInfosContainerEl.querySelector(".current--info");
	let previousInfoEl = cardInfosContainerEl.querySelector(".previous--info");
	let nextInfoEl = cardInfosContainerEl.querySelector(".next--info");

	gsap.timeline()
		.to([buttons.prev, buttons.next], {
		duration: 0.2,
		opacity: 0.5,
		pointerEvents: "none",
	})
		.to(
		currentInfoEl.querySelectorAll(".text"),
		{
			duration: 0.4,
			stagger: 0.1,
			translateY: "-120px",
			opacity: 0,
		},
		"-="
	)
		.call(() => {
		swapInfosClass(direction);
	})
		.call(() => initCardEvents())
		.fromTo(
		direction === "right"
		? nextInfoEl.querySelectorAll(".text")
		: previousInfoEl.querySelectorAll(".text"),
		{
			opacity: 0,
			translateY: "40px",
		},
		{
			duration: 0.4,
			stagger: 0.1,
			translateY: "0px",
			opacity: 1,
		}
	)
		.to([buttons.prev, buttons.next], {
		duration: 0.2,
		opacity: 1,
		pointerEvents: "all",
	});

	function swapInfosClass() {
		currentInfoEl.classList.remove("current--info");
		previousInfoEl.classList.remove("previous--info");
		nextInfoEl.classList.remove("next--info");

		if (direction === "right") {
			currentInfoEl.classList.add("previous--info");
			nextInfoEl.classList.add("current--info");
			previousInfoEl.classList.add("next--info");
		} else if (direction === "left") {
			currentInfoEl.classList.add("next--info");
			nextInfoEl.classList.add("previous--info");
			previousInfoEl.classList.add("current--info");
		}
	}
}

function updateCard(e) {
	const card = e.currentTarget;
	const box = card.getBoundingClientRect();
	const centerPosition = {
		x: box.left + box.width / 2,
		y: box.top + box.height / 2,
	};
	let angle = Math.atan2(e.pageX - centerPosition.x, 0) * (35 / Math.PI);
	gsap.set(card, {
		"--current-card-rotation-offset": `${angle}deg`,
	});
	const currentInfoEl = cardInfosContainerEl.querySelector(".current--info");
	gsap.set(currentInfoEl, {
		rotateY: `${angle}deg`,
	});
}

function resetCardTransforms(e) {
	const card = e.currentTarget;
	const currentInfoEl = cardInfosContainerEl.querySelector(".current--info");
	gsap.set(card, {
		"--current-card-rotation-offset": 0,
	});
	gsap.set(currentInfoEl, {
		rotateY: 0,
	});
}

function initCardEvents() {
	const currentCardEl = cardsContainerEl.querySelector(".current--card");
	currentCardEl.addEventListener("pointermove", updateCard);
	currentCardEl.addEventListener("pointerout", (e) => {
		resetCardTransforms(e);
	});
}

initCardEvents();

function removeCardEvents(card) {
	card.removeEventListener("pointermove", updateCard);
}

function init() {

	let tl = gsap.timeline();

	tl.to(cardsContainerEl.children, {
		delay: 0.15,
		duration: 0.5,
		stagger: {
			ease: "power4.inOut",
			from: "right",
			amount: 0.1,
		},
		"--card-translateY-offset": "0%",
	})
		.to(cardInfosContainerEl.querySelector(".current--info").querySelectorAll(".text"), {
		delay: 0.5,
		duration: 0.4,
		stagger: 0.1,
		opacity: 1,
		translateY: 0,
	})
		.to(
		[buttons.prev, buttons.next],
		{
			duration: 0.4,
			opacity: 1,
			pointerEvents: "all",
		},
		"-=0.4"
	);
}

const waitForImages = () => {
	const images = [...document.querySelectorAll("img")];
	const totalImages = images.length;
	let loadedImages = 0;
	const loaderEl = document.querySelector(".loader span");

	gsap.set(cardsContainerEl.children, {
		"--card-translateY-offset": "100vh",
	});
	gsap.set(cardInfosContainerEl.querySelector(".current--info").querySelectorAll(".text"), {
		translateY: "40px",
		opacity: 0,
	});
	gsap.set([buttons.prev, buttons.next], {
		pointerEvents: "none",
		opacity: "0",
	});

	images.forEach((image) => {
		imagesLoaded(image, (instance) => {
			if (instance.isComplete) {
				loadedImages++;
				let loadProgress = loadedImages / totalImages;

				gsap.to(loaderEl, {
					duration: 1,
					scaleX: loadProgress,
					backgroundColor: `hsl(${loadProgress * 120}, 100%, 50%`,
				});

				if (totalImages == loadedImages) {
					gsap.timeline()
						.to(".loading__wrapper", {
						duration: 0.8,
						opacity: 0,
						pointerEvents: "none",
					})
						.call(() => init());
				}
			}
		});
	});
};

waitForImages();

	})

  