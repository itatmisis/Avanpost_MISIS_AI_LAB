


$(function () {
    const form = document.querySelector("form"),
        fileInput = document.querySelector(".file-input")

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
            xhr.open("POST", "http://localhost:5002/UploadImages");

            let data = new FormData();
            console.log(form[0].files);

            let totalSize = 0;
            $.each(form[0].files, function (i, file) {
                data.append('file', file);
                totalSize += file.size;
            });

            data.append("request", JSON.stringify({ ClassName: "1111" }))

            xhr.upload.onprogress = ({ loaded, total }) => {
                let fileLoaded = Math.floor((loaded / totalSize) * 100);
                console.log(fileLoaded)
                changeProgressBarValue(fileLoaded)
                uploadedArea.classList.add("onprogress");
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


})

function createGraph(startingIntent, story) {
    if (!graph) {
        addPan()
        window.addEventListener('resize', () => {
            updateLines()
        })
    } else {
        graph.remove()
    }

    graph = renderIntentAction(startingIntent, story)
    document.getElementById('graph-root')?.appendChild(graph)
    updateTippy()
    addPan()
    updateLines()
}


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


