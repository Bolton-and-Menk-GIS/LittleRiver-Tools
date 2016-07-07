globObj = {};

var getData = (function() {
  var data = {};
  var info = {};
  var newRec, editRecs;

  function getJSON(qry) {

    function fq(val) {
      var ownCode = /^[a-z]{4}[0-9]{2}$/i
      var pinPat = /^[0-9\-.]+$/

      if (ownCode.test(val)) {
        return "owner_code=" + val.toUpperCase();
      } else if (pinPat.test(val)) {
        return "pin=" + val.replace(/[-.]/g, "");
      } else {
        return "owner=" + val
      }
    }
    var code = fq(qry);

    var uri = 'http://localhost:5001/rest/query?' + code

    console.log('uri: ', uri)

    // var uri = 'http://localhost:5001/rest/query?owner=' + owner + '&county=bollinger'
    LocalUtils.getJson(uri, 'jsonp', 'POST').done(function(res) {
      console.log("DATA", res);
      var info = {};

      info.attributes = getInfo(res);

      data.attributes = info.attributes;

      bldSrchTbl(info.attributes);
      console.log('info', info)

      data.fieldMaps = getFields(res[0]);
    });
  }

  function getInfo(res, fields) {
    var info = res.map(function(v, idx) {
      var dateFix = LocalUtils.formatDate(v.attributes.DATE_PAID);
      var amountPaid = LocalUtils.toFixed(v.attributes.AMOUNT_PAID);
      // v.attributes.date = dateFix.outputDate;
      // v.attributes.amountPaid = amountPaid
      v.attributes.DATE_PAID = LocalUtils.formatDate(v.attributes.DATE_PAID).outputDate;
      v.attributes.AMOUNT_PAID = amountPaid
      v.attributes.ASSESSED_ACRES = LocalUtils.toFixed(v.attributes.ASSESSED_ACRES);
      return v.attributes;
    });
    return info
  }

  function getFields(res) {
    var propsArray = [];
    var props = Object.getOwnPropertyNames(res.attributes)

    $('#summary').children().children().children().each(function(val, a) {
      console.log("SUMMARY TABVLE FIELDS: ", val, $(a).text())
    });
    return props;
  }

  function getEditRecords(rec) {
    // BECAUSE WHEN YOU PASS UP 
    console.log("RECLA>A>>", rec)
    if (!(rec)) {
      console.log("YOUYO")
      newRec = {};
      editRecs = {};
      newRec.PIN = 'null';
      newRec.newRecord = 'NewRecord';
      $('#summary').children().children().find('td').each(function(ind, val) {
        console.log("IND: ", this.id, "Val", $(this).html());
        // editRecs[this.id] = $(this).html();
        var idx = $(this).attr('idx');
        if (idx == 'DATE_PAID' && $('#dp').datepicker().val()) {
          newRec[idx] = $('#dp').datepicker().val();
        } else if (idx == 'PAID' && !$('#soflow').val()) {
          console.log('PAID!!!!!!', $(this).html())
          newRec[idx] = $(this).html();
        } else if (idx == 'PAID' && $('#soflow').val()) {
          newRec[idx] = $('#soflow').val();
        } else {
          newRec[idx] = $(this).html();
        }
      });

    } else {

      console.log("REC????????", rec)
      newRec = {};
      editRecs = {};
      Object.keys(rec).forEach(function(key) {
        editRecs[key] = rec[key];
        newRec.PIN = rec.PIN;
        $('#summary').children().children().find('td').each(function(ind, val) {
          if (key == $(this).attr('idx')) {
            if (key == 'DATE_PAID' && $('#dp').datepicker().val()) {
              newRec[key] = $('#dp').datepicker().val();
              editRecs[key] = $('#dp').datepicker().val();
            } else if (key == 'PAID' && !$('#soflow').val()) {
              console.log('PAID!!!!!!')
              newRec[key] = $(this).html();
            } else if (key == 'PAID' && $('#soflow').val()) {
              newRec[key] = $('#soflow').val();
            } else {
              newRec[key] = $(val).html();
              editRecs[key] = $(val).html();
            }
          }
        });
      });
    }
    return {
      'NewRec': newRec,
      'AllRec': editRecs
    }
  }

  function editCall(updates, adds) {
    console.log('adds::: ', updates)
    updates = JSON.stringify(updates);
    adds = JSON.stringify(adds);


    var update = {
      updates: updates,
       adds: adds
    }
    // var add = {
    //   adds: adds
    // }

    // var adds = {adds: adds}

    console.log('UPDATES??? ', updates)

    var uri = 'http://localhost:5001/rest/applyEdits'
    LocalUtils.getJson(uri, 'jsonp', 'POST', update).done(function(res) {
      console.log(res);
    })

  }

  return {
    getJSON: function(owner) {
      getJSON(owner);
      return {
        data: data,
        info: info
      }
    },
    getData: function() {
      return {
        data: data,
        info: info
      }
    },
    getEdits: function(rec) {
      var editRecs = getEditRecords(rec);
      console.log("EDIT RECORDS??? ", editRecs);
      return {
        data: data,
        info: info,
        edits: editRecs
      }
    },
    getEditData: function() {
      return {
        data: data,
        edits: {
          NewRec: newRec,
          EditRec: editRecs
        }
      }
    },
    postEdits: function(updateList, addList) {
      var posts = editCall(updateList, addList);
    }
  }
})();