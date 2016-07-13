
var Voice = function() {};

Voice.prototype.recognizing = false;
Voice.prototype.recognition = null;
Voice.prototype.ignore_onend = false;

Voice.prototype.speak = function(text) {
   var msg = new SpeechSynthesisUtterance();
   var voices = speechSynthesis.getVoices();
   msg.voice = voices[10];
   msg.voiceURI = 'native';
   msg.volume = 1;
   msg.rate = 1;
   msg.pitch = 1;
   msg.text = text;
   msg.lang = 'es-ES';
   speechSynthesis.speak(msg);
}

Voice.prototype.init = function(proc_text_callback) {
   if ('webkitSpeechRecognition' in window) {
      Voice.prototype.recognition = new webkitSpeechRecognition();
      Voice.prototype.recognition.continuous = true;
      Voice.prototype.recognition.interimResults = true;

      Voice.prototype.recognition.onstart = function() {
         Voice.prototype.recognizing = true;
         start_img.src = '/ui/images/mic-animate.gif';
      };

      Voice.prototype.recognition.onerror = function(event) {
         if (event.error == 'no-speech') {
            start_img.src = '/ui/images/mic.gif';
            this.ignore_onend = true;
         }

         if (event.error == 'audio-capture') {
            start_img.src = '/ui/images/mic.gif';
            this.ignore_onend = true;
         }

         if (event.error == 'not-allowed') {
            this.ignore_onend = true;
         }
      };

      Voice.prototype.recognition.onend = function() {
         Voice.prototype.recognizing = false;
         if (Voice.prototype.ignore_onend) {
            return;
         }
       
         start_img.src = '/ui/images/mic.gif';
      };

      Voice.prototype.recognition.onresult = function(event) {
         var interim_transcript = '';
         if (typeof(event.results) == 'undefined') {
            Voice.prototype.recognition.onend = null;
            Voice.prototype.recognition.stop();
            return;
         }

         for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
               var text=event.results[i][0].transcript;
               proc_text_callback(text);
            } 
         }
      };
   }
};


Voice.prototype.recognition_start = function() {
   if(!Voice.prototype.recognizing);
   {  
      Voice.prototype.recognition.lang = 'es-ES';
      Voice.prototype.recognition.start();
      this.ignore_onend = false;
      start_img.src = '/ui/images/mic-slash.gif';
   }
};

Voice.prototype.recognition_stop = function() {
   if(Voice.prototype.recognizing);
      Voice.prototype.recognition.stop();
};

