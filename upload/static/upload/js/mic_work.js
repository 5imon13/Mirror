var infoBox;
// var textBox; 
// var tempBox;
var startStopButton; // 「辨識/停止」按鈕
var final_transcript = '';
var recognizing = false;
// var camera_word = ['相機', '鏡頭'];
// var image_word = ['上傳','照片'];
// var login_word = ['登入', '使用者'];
var keyword_arr = ['登入', '上一頁', '選擇', '推薦', '單寧', '商務', '運動', '首頁', '丹尼', '丹寧'];
var key_word;


function startButton(event) {
    console.log('start_r1');
    infoBox = document.getElementById("infoBox");
    // textBox = document.getElementById("textBox"); 
    // tempBox = document.getElementById("tempBox");
    
    startStopButton = document.getElementById("startStopButton"); 
    
    langCombo = "cmn-Hant-TW";
    console.log('start_r2');
    if (recognizing) {                      // if recognizing, stop it
        startStopButton.className = startStopButton.className.replace(/\bmic_icon_working\b/g, "mic_icon");
        recognition.stop();
    }
    else {                                  // start recognizing
        startStopButton.className = startStopButton.className.replace(/\bmic_icon\b/g, "mic_icon_working"); 
        console.log('start_r3');
        // textBox.value = ''; // 清除最終的辨識訊息
        // tempBox.value = '';
        final_transcript = '';              // 最終的辨識訊息變數
        recognition.lang = "cmn-Hant-TW";   // 設定辨識語言
        recognition.start();
        console.log('start_r4');
    }
}

if (!('webkitSpeechRecognition' in window)) {  
    infoBox.innerText = "本瀏覽器不支援語音辨識，請更換瀏覽器！(Chrome 25 版以上才支援語音辨識)";
} 
else {
    
    var recognition = new webkitSpeechRecognition(); // 建立語音辨識物件 webkitSpeechRecognition
    recognition.continuous = true;                   // 設定連續辨識模式
    recognition.interimResults = true;
    console.log('enter_elseLoop');

    recognition.onstart = function() {               // 開始辨識
        recognizing = true;
        console.log('start_record');
        // infoBox.innerText = "辨識中...";
    };
    recognition.onend = function() {                 // 辨識完成
        recognizing = false;
<<<<<<< HEAD
        console.log('end_record');
=======
>>>>>>> c5af44ac56cc9286e86a137085aaf2837794de36
        // infoBox.innerText = "";
    };
    recognition.onresult = function(event) {                // 辨識有任何結果時
        var interim_transcript = '';                                        // 中間結果
        for (var i = event.resultIndex; i < event.results.length; ++i) { // 對於每一個辨識結果
            if (event.results[i].isFinal) {                              // 如果是最終結果
                final_transcript += event.results[i][0].transcript; // 將其加入最終結果中
            } 
            else { 
                interim_transcript += event.results[i][0].transcript; // 將其加入中間結果中
            }
        }
        if (interim_transcript.trim().length > 0) {
            console.log(interim_transcript.trim())
            for (i = 0; i < keyword_arr.length; i++) {
                if (interim_transcript.trim().includes(keyword_arr[i])) {
                    switch (i) {
                        case 0 :   
                            window.location = '/upload/login/';
                            break;
                        case 1 : case 4 :
                            window.location = '/upload/';
                            break;
                        case 2 :
                            console.log(window.location.href)
                            if (window.location.href.includes('result')){
                                console.log('result_page_get')
                            }
                            //document.getElementById('select_bar').click;
                            break;
                        case 3 :
                            if (window.location.href.includes('result')){
                                if (document.getElementById('select_bar').value != '推薦風格'){
                                    document.getElementById('clothes_btn').click();
                                };
                            };
                            break;
                        case 4 : case 8 : case 9 :     
                            if (window.location.href.includes('result')){                        
                                document.getElementById('select_bar').selectedIndex = '1';
                            };
                            break;
                        case 5 :         
                            if (window.location.href.includes('result')){                    
                                document.getElementById('select_bar').selectedIndex = '2';
                            };
                            break;
                        case 6 :   
                            if (window.location.href.includes('result')){                          
                                document.getElementById('select_bar').selectedIndex = '3';
                            };
                            break;
                        default :
                            console.log('no_keyword');
                    };
                };
            };                
        };
        // if (final_transcript.trim().length > 0) {
        //     // textBox.value = final_transcript;
        //     infoBox.value = final_transcript;
        // };
    };
};