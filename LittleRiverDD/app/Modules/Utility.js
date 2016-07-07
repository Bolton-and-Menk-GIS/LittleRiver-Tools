var LocalUtils = (function() {
  return {
    formatDate: function(date) {
      var inputDate = new Date(date);
      var today = new Date();
      var currDay = today.getDate();
      var currMonth = today.getMonth();
      var currYear = today.getFullYear();
      var outputDay = inputDate.getDate();
      var outputMonth = inputDate.getMonth();
      var outputYear = inputDate.getFullYear();
      currMonth = currMonth + 1;
      outputMonth = outputMonth + 1;
      return {
        outputDate: outputMonth + '/' + outputDay + '/' + outputYear,
        currentDate: currMonth + '/' + currDay + '/' + currYear
      }
    },
    URIquery: function(a) {
      var queryURI = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i) {
          var p = a[i].split('=', 2);
          if (p.length == 1)
            b[p[0]] = "";
          else
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
      })(window.location.search.substr(1).split('&'));
      return queryURI
    },
    getJson: function(url, dataType, method, data) {
      var jqxhr = $.ajax({
        url: url,
        dataType: dataType,
        method: method,
        data: data,
        error: function(xhr, textStatus, errorThrown) {
          console.log("ERROR THROWN: ", errorThrown)
          if (textStatus == 'timeout') {
            this.tryCount++;
            if (this.tryCount <= this.retryLimit) {
              $.ajax(this);
              return;
            }
            return;
          }
          if (xhr.status == 500) {
            //handle error
          } else {
            //handle error
          }
        }
      })
      return jqxhr
    },
    toFixed: function(val) {
      if (val) {
        return val.toFixed(2)
      } else {
        return 0
      }
      return val;
    },
    isInt: function(inp) {
      return inp % 1 === 0
    },
    attachFiles: function(evt, el) {
      if (window.File && window.FileReader && window.FileList && window.Blob) {
        console.log("SUPPORTED!")
        var files = evt.files;

        var fileArray = [];

        Object.keys(files).forEach(function(val) {
          console.log("VALL", files[val]);

          if (files[val].type.match('image.*')) {
            console.log("IMAGE");

            var reader = new FileReader();

            console.log(reader)
            reader.onload = (function(file) {
              return function(e) {
                console.log("EEE? ", e)
                $(el).append('<span id="imgAttch' + val + '"></span');
                $('#imgAttch' + val).html('<img class = "thumb" src="' + e.target.result + '"/>');
              }
            })(files[val]);
            // Read in the image file as a data URL.
            reader.readAsDataURL(files[val]);
            fileArray.push(files);
          }

        })
      } else {
        alert('The File APIs are not fully supported in this browser.');
      }
      return fileArray;
    }
  }
})();