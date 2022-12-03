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
            xhr.open("POST", "https://localhost:7002/UploadImages");

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

    getClassesToTrain();
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
    $(".progress-bar").css("visibility", "hidden");
}

function changeProgressBarValue(percents) {
    $(".progress-bar").html(`${percents}%`);
    $(".progress-bar").css('width', `${percents}%`)
}

function getClassesToTrain() {
    $.ajax({
        url: 'http://213.178.155.140:8000/UploadImages/Upload',
        method: 'get',
        dataType: 'json',
        success: function (data) {
            showClassesData(data)
        },
        error: function (error) {
            console.log(error)
        }
    });
}

function showClassesData(data) {
    if (data.length > 0) {
        showClasses();

    }
    else {
        showNoClasses();
    }
}

function showNoClasses() {
    $(".zero-models").css("display", "inherit")
    $(".data-classes").css("display", "none")
}

function showClasses() {
    $(".zero-models").css("display", "none")
    $(".data-classes").css("display", "inherit")
}


