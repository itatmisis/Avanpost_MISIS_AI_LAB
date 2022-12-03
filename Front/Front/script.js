$(function () {
    const form = document.querySelector("form"),
        fileInput = document.querySelector(".file-input")
    getClassesToTrain()

    $(document).ready(function () {
        ToAddClass();
        // const startingIntent = 'Модель';
        // const mergedStory = {'Модель': 'версия 1'}
        // createGraph(startingIntent, mergedStory[startingIntent])

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
            xhr.open("POST", "http://213.178.155.140:8000/UploadImages");

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

                }
            }


            xhr.send(data);
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

    $(document).on('click',
        '.to-test-model',
        function () {
            ToModelTestTable();
        })

    $('#parser').click(function () {
        if ($(this).is(':checked')) {
            $('.image-number').show(100);
        } else {
            $('.image-number').hide(100);
        }
    });

    $('.number-control').on('change', function () {
        console.log(parseInt(document.querySelector(".number-control").value))
        if (parseInt(document.querySelector(".number-control").value) > 0 ) {
            $('.add-class-btn').prop('disabled', false);
        }
        else {
            $('.add-class-btn').prop('disabled', true);
        }
    });

    $(document).ready(function () {
        $('.add-class-btn').prop('disabled', true);
        $('.image-number').hide();
        //document.querySelector(".form-control")
        // console.log(document.querySelector(".form-control").value, form.value)
        // if(document.querySelector(".form-control").value != '' && form.value) {
        //     $('.add-class-btn').prop('disabled', false);
        // }
    });
})


function ToAddClass() {
    $(".body-add-class").css("display", "inherit");
    $(".body-train").css("display", "none");
    $(".body-version-history").css("display", "none");
    $(".body-model-test").css("display", "none");
    $(".to-add-class").css("color", "#6990F2");
    $(".to-train").css("color", "black");
    $(".to-model-version").css("color", "black");
    $(".to-test-model").css("color", "black");
}

function ToTrainTable() {
    $(".body-add-class").css("display", "none");
    $(".body-train").css("display", "inherit");
    $(".body-version-history").css("display", "none");
    $(".body-model-test").css("display", "none");
    $(".to-add-class").css("color", "black");
    $(".to-train").css("color", "#6990F2");
    $(".to-model-version").css("color", "black");
    $(".to-test-model").css("color", "black");
}

function ToVersionHistoryTable() {
    $(".body-add-class").css("display", "none");
    $(".body-train").css("display", "none");
    $(".body-version-history").css("display", "inherit");
    $(".body-model-test").css("display", "none");
    $(".to-add-class").css("color", "black");
    $(".to-train").css("color", "black");
    $(".to-model-version").css("color", "#6990F2");
    $(".to-test-model").css("color", "black");
}

function ToModelTestTable() {
    $(".body-add-class").css("display", "none");
    $(".body-train").css("display", "none");
    $(".body-version-history").css("display", "none");
    $(".body-model-test").css("display", "inherit");
    $(".to-add-class").css("color", "black");
    $(".to-train").css("color", "black");
    $(".to-model-version").css("color", "black");
    $(".to-test-model").css("color", "#6990F2");
}


function showProgressBar() {
    $(".progress-bar").css("visibility", "visible");
}

function hideProgressBar() {
    $(".progress-bar").css("visibility", "hidder");
}

function changeProgressBarValue(percents) {
    $(".progress-bar").html(`${percents}%`);
    $(".progress-bar").css('width', `${percents}%`)
}

function getClassesToTrain() {
    $.ajax({
        url: 'http://213.178.155.140:8000/DataClasses/AllClasses',
        method: 'get',
        dataType: 'json',
        success: function (data) {
            //alert(data);
            console.log(data)
            // $(".choose-models").css("display", "inherit");
            $(".zero-models").css("display", "none");
        }
    });
}

$(document).ready(function () {
  
    // build the gallery
    $("#my_nanogallery2").nanogallery2({
      thumbnailSelectable :   true,   // enables selection mode
      items:[
        {
          src:   'berlin1.jpg',     // image url
          srct:  'berlin1t.jpg',    // thumbnail url
          title: 'Berlin 1'         // element title
        },
        { src: 'berlin2.jpg', srct: 'berlin2t.jpg', title: 'Berlin 2' },
        { src: 'berlin3.jpg', srct: 'berlin3t.jpg', title: 'Berlin 3' }
      ],
      thumbnailWidth:         'auto',
      thumbnailHeight:        150,
      itemsBaseURL: 'https://nanogallery2.nanostudio.org/samples/',
      thumbnailHoverEffect2: null,
      locationHash: false
    })
    $(".nGY2GallerySub").css({"overflow": "visible", "touch-action": "pan-y", "user-select": "none", "-webkit-user-drag": "none", "-webkit-tap-highlight-color": "rgba(0, 0, 0, 0)", "transform": "none", "width": "700px", "height": "158px"})
  
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
  
  });