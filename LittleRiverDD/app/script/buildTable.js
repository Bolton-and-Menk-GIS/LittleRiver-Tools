// BUILD TABLE
$(function() {
  var inp;

  $('#search').keypress(function(evt) {
    evt.stopPropagation();
    if (evt.which == 13) {
      $('#searchButton').click();
    }
  });

  // SEARCH BUTTON
  $('#searchButton').click(function() {
    // search()
    $('.srchTbl').remove();
    inp = $('#search').val();
    getData.getJSON(inp);
  });

  // SUBMIT BUTTON
  $('#stageEdits').click(function() {
    // NEW RECORD 
    if ($('#summary').children().children().hasClass('newRec')) {
      var dataAttr = getData.getData().data;
      var rec = null;
      var recs = getData.getEdits(rec);
      // PIN VALIDATION //
           if ('NewRec' in recs.edits){
                if (!recs.edits.NewRec.PARCEL_ID){
                     alert('You must enter a valid Parcel ID for record!');
                     var pidBox = $('.nr[idx="PARCEL_ID"]')[0]
                     // tried to simulate click here to start an edit, no dice
                     pidBox.click()
                     pidBox.focus();
           
                     return
                }else {
                     recs.edits.NewRec.PIN = recs.edits.NewRec.PARCEL_ID.replace(/[-.]/g, "")
                }
           }
      // PIN VALIDATION //      
      globObj.editRecs = recs;
      buildEditTbl(recs.edits, 'newRec');

      // :::: EFFECTS :::: 
      $('.newRec').remove();
      // $('.newRec').fadeOut();
      // :::: EFFECTS :::: 
    } else {
      // EXISTING RECORD (EDIT)
      var id = $('.smryTbl').attr('idx');
      // var recs = getEditRecords(globObj.attributes[id]);
      var dataAttr = getData.getData().data
      var recs = getData.getEdits(dataAttr.attributes[id]);
      globObj.editRecs = recs;
      buildEditTbl(recs.edits, id);
      // buildTable($('#editList'), 'edtbl', recs.NewRec, id);
      globObj.editRecs = recs;

      // :::: EFFECTS :::: 
      // $('.smryTbl').remove();
      $('.smryTbl').fadeOut();
      // :::: EFFECTS :::: 
    }

    displayBtn();

  });

  // ADD NEW RECORD
  $('#addNew').click(function() {
    $('#newRec').children().eq(0).focus();
    $('.smryTbl').remove();
    $('.newRec').remove();


    $('#summary').children().append('<tr class="newRec" id="newRec"><td class="nr" idx="OWNER"></td><td class="nr" idx="OWNER_CODE"></td><td class="nr" idx="PARCEL_ID"></td><td class="nr" idx="ASSESSED_ACRES"></td><td class="nr" idx="DATE_PAID" id="DATE_PAID"></td><td class="nr" idx="YEAR"></td><td class="nr" idx="PENALTY"></td><td class="nr" idx="AMOUNT_PAID"></td><td class="nr" id="PAID" idx="PAID"></td><td class="nr" idx="EXCESS"></td><td class="nr" idx="ASSESSED_ACRES"></td><td class="nr" idx="TOT_BENEFIT"></td></tr>');
    // $('.smryTbl').append('<td class="moveDown" id="ZA"><i id="moveDown" class="fa fa-arrow-circle-down" aria-hidden="true" data-toggle="tooltip" style="font-size: 24px"></i></td>')

    // DATE STUFF
    $('#DATE_PAID').one('click', function() {
      datepicker($(this));
    })

    $('#PAID').one('click', function() {
        dropDown($(this));
      })
      // DATE STUFF


    $('#summary').children().children().find('td').one('click', function(event) {
      if ($(this).hasClass('smryData')) {
        $(this).removeClass('smryData')
      }

      $(this).siblings().removeClass('smryData');
      $(this).addClass('smryData');
      $('#mvdn').removeClass('smryData');
      var fm = $(this).html();

    console.log("NEW REC EL ", $($(this)[0]).attr('idx'))

   var width = '65px';

    if (($($(this)[0]).attr('idx') == 'PARCEL_ID') || ($($(this)[0]).attr('idx') == 'OWNER')) {
      console.log("LONG FIELD")
      width = '200px';
    }

      var rw = $('<input type="text" tabindex="1" class="newRec" id="input0" placeholder="Add New Record" value="' + fm + '" style="width:'+width+'">');
      var cw = $('input[name="hiddenField"]');
      $(this).inlineEdit(rw, cw);
      displayBtn();
    });
  });

  $('#postEdits').click(function() {
    processEdits(editList);
  });
});

function datepicker(el) {
  el.empty();
  el.append('<input type="text" class="inpt" id="dp" style="width: 70px; height: 20px; padding: 3px; padding-bottom: 0px; padding-top:0px">')
  $('#dp').datepicker({
    dateFormat: "m/dd/yy"
  });
}

function dropDown(el) {
  el.empty();
  el.append('<div><select id="soflow"><option select>Y</option><option>N</option></select></div>');
}


$.fn.inlineEdit = function(RW, CW) {
  $(this).click(function() {
    if (this.id == 'DATE_PAID' || this.id == 'PAID' || this.id == 'mvdn') {} else {

      var el = $(this);

      el.siblings().removeClass('smryData');
      el.hide();
      el.after(RW);
      RW.focus();

      RW.blur(function() {
        if ($(this).val() != "") {
          CW.val($(this).val()).change();
          el.text($(this).val());
        }

        $(this).remove();

        el.after().addClass('smryData');
        el.siblings().removeClass('smryData');

        el.show();
      });
    }
  });

}

var editList = [];

function buildEditTbl(recs, idx) {
  var rec = recs.NewRec
    // $('#editList').append('<tr class="edtbl" id='+idx+'><td id="OWNER">'+rec.OWNER+'</td><td id="PARCEL_ID">'+rec.PARCEL_ID+'</td><td id="amountPaid">'+rec.amountPaid+'</td><td id="date">'+rec.date+'</td><td id="PENALTY"></td><td id="TOT_ADMIN_FEE"></td><td id="PAID"></td><td id="EXCESS"></td></tr>');
  buildTable($('#editList'), 'edtbl', rec, idx);
  $('#editView').slideDown();

  editList.push(rec);
}

function bldSummaryBox(code) {
  var getInfo = getData.getOwnerInfo(code);

  // var information = getInfo.promise(function(res){
  //   console.log("RESULT PROMISE: ", res)
  // })

  var uri = 'http://localhost:5001/rest/getOwnerSummary?code=' + code;
  var info = LocalUtils.getJson(uri, 'jsonp', 'POST').done(function(res) {

    console.log('RES? ', res)
    // format Data
    var TadminFee = LocalUtils.toFixed(res.total_admin_fee);
    var totalBill = LocalUtils.toFixed(res.total_bill);
    var assmnt = LocalUtils.toFixed(res.total_assessment);
    // var countyAbbrv = res.county

    var countyAbbrv = res.county.replace('COUNTY', '');

    console.log("CA: ", countyAbbrv)

    // BUILD LB TABLE
    $('.tblData').empty();
    $('#AF').children().children().find('td').remove();
    $('#ownerData').append(res.code);
    $('#nameData').append(res.name);
    $('#dpData').append('7/7/2016');
    $('#adminFeeData').append('$' + TadminFee);
    $('#billData').append('$' + totalBill);
    $('#assessData').append('$' + assmnt);
    $('#penData').append('$' + res.penalty);
    $('#countyData').append(countyAbbrv);
    res.assessments.map(function(va) {
      var adminFee = LocalUtils.toFixed(va.admin_fee);
      $('#AF').append('<tr><td class="tblData" style="padding-left: 10px">' + va.pin + '</td><td class="tblData" style="padding-left: 10px">$' + adminFee + '</td></tr>');
    })

  });

  LightBox($('<div id="lb-content"></div>'));
  $('#lb-content').append($('#summaryView'));
  $('#lb-content').show();
  $('#summaryView').css('display', 'block');
}

function bldSmryTbl(rec, idx, newRecord) {
  if (!rec) {}
  $('.smryTbl').remove();
  if (newRecord) {
    buildTable($('#summary'), 'smryTbl', rec, idx, newRecord);
  } else {
    // $('#summary').append('<tr class="smryTbl" id='+idx+'><td id="OWNER">'+rec.OWNER+'</td><td id="PARCEL_ID">'+rec.PARCEL_ID+'</td><td id="amountPaid">$'+rec.amountPaid+'</td><td id="date">'+rec.date+'</td><td id="PENALTY">a</td><td id="TOT_ADMIN_FEE"></td><td id="PAID"></td><td id="EXCESS"></td></tr>');
    buildTable($('#summary'), 'smryTbl', rec, idx);
  }

  $('.smryTbl').children().one("click", function(event) {


    $(this).siblings().removeClass('smryData');
    $(this).addClass('smryData');

    var fm = $(this).html();

    console.log("HUH ", $($(this)[0]).attr('idx'))

    var width = '65px';

    if (($($(this)[0]).attr('idx') == 'PARCEL_ID') || ($($(this)[0]).attr('idx') == 'OWNER')) {
      console.log("LONG FIELD")
      width = '200px';
    }

    var rw = $('<input type="text" class="inpt" data-id="'+$($(this)[0]).attr('idx')+'" id="input' + idx + '" value="' + fm + '" style="width: '+width+'">');

    // $(rw).id()
    console.log('RW VALUE ', rw[0])
    // $('.nr[idx="PARCEL_ID"]')[0]

    var cw = $('input[name="hiddenField"]');
    $(this).inlineEdit(rw, cw);
    //<input type="text" id="row-1-age" name="row-1-age" value="61">
  });
  displayBtn();
  //OWNER_CODE
}


function displayBtn() {
  if ($('#summary').children().children().find('td').length > 0) {
    $('#stageEdits').css('display', 'inline');
    $('#btnContainer').css('width', '65px');
  } else {
    $('#stageEdits').css('display', 'none');
    $('#btnContainer').css('width', '28px');
  }
}

function bldSrchTbl(res) {
  res.forEach(function(v, idx) {
    buildTable($('#srchRslt'), 'srchTbl', v, idx);
    // $('#srchRslt').append('<tr class="srchTbl" id='+idx+'><td id="OWNER">'+v.OWNER+'</td><td id="PARCEL_ID">'+v.PARCEL_ID+'</td><td id="amountPaid">$'+v.amountPaid+'</td><td id="date">'+v.date+'</td></tr>');
  });

  $('.more').click(function(evt) {
    evt.stopPropagation();
    var gid = $(this).parent()[0].id
    bldSummaryBox(gid)
  })

  $('.srchTbl').click(function(a) {
    $('.newRec').remove()
    var idx = $(this).attr('idx');
    bldSmryTbl(res[idx], idx);
  });
}

var counter = (function() {
  var _privateCounter = 0;

  function changeBy(val) {
    _privateCounter += val;
  }

  function reset() {
    _privateCounter = 0;
  }
  return {
    increment: function(val) {
      changeBy(val);
    },
    decrement: function() {
      changeBy(-1);
    },
    reset: function() {
      reset();
    },
    value: function() {
      return _privateCounter;
    }
  };
})();

function buildTable(el, type, v, idx, newRecord) {
  // counter.increment(1);
  if (type == 'smryTbl') {
    $('.newRec').remove();
    if (newRecord) {
      el.append('<tr class="' + type + ' newRec" idx=' + idx + ' id=' + v.OWNER_CODE + '><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td  idx="ASSESSED_ACRES">' + v.ASSESSED_ACRES + '</td><td id="DATE_PAID" idx="DATE_PAID">' + v.DATE_PAID + '</td><td id="YEAR" idx="YEAR">' + v.YEAR + '</td><td idx="PENALTY">' + v.PENALTY + '</td><td id="AMOUNT_PAID" idx="AMOUNT_PAID">' + v.AMOUNT_PAID + '</td><td id="PAID" idx="PAID">' + v.PAID + '</td><td idx="EXCESS">' + v.EXCESS + '</td><td idx="ASSESSED_ACRES">' + v.ASSESSED_ACRES + '</td><td idx="TOT_BENEFIT">' + v.TOT_BENEFIT + '</td></tr>');
    } else {
      el.append('<tr class="' + type + '" idx=' + idx + ' id=' + v.OWNER_CODE + '><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td idx="ASSESSED_ACRES">' + v.ASSESSED_ACRES + '</td><td id="DATE_PAID" idx="DATE_PAID">' + v.DATE_PAID + '</td><td id="YEAR" idx="YEAR">' + v.YEAR + '</td><td idx="PENALTY">' + v.PENALTY + '</td><td id="AMOUNT_PAID" idx="AMOUNT_PAID">' + v.AMOUNT_PAID + '</td><td id="PAID" idx="PAID">' + v.PAID + '</td><td idx="EXCESS">' + v.EXCESS + '</td><td idx="ASSESSED_ACRES">' + v.ASSESSED_ACRES + '</td><td idx="TOT_BENEFIT">' + v.TOT_BENEFIT + '</td></tr>');
    }
    // $('.smryTbl').append('<td class="moveDown" id="mvdn"><i id="stageEdits" class="fa fa-arrow-circle-down" aria-hidden="true" data-toggle="tooltip" style="font-size: 24px"></i></td>')

  } else {
    if (!(v.PIN)) {
      counter.increment(1);
      el.append('<tr class="' + type + '" idx=' + idx + ' id=nr' + counter.value() + '><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td idx="ASSESSED_ACRES">' + v.ASSESSED_ACRES + '</td><td idx="DATE_PAID">' + v.DATE_PAID + '</td><td idx="PENALTY">' + v.PENALTY + '</td><td id="AMOUNT_PAID" idx="AMOUNT_PAID">' + v.AMOUNT_PAID + '</td><td idx="PAID">' + v.PAID + '</td></tr>')
    } else {
      var values = {};

      Object.keys(v).forEach(function(key) {
          values[key] = v[key];
          if (v[key] == null) {
            // values[key] = 'No Value';
            // v[key] = 'No Value'
            // values[key] = 'No Value';

          }
        })
        // THIS TABLE DEFINITION REPRESENTS SEARCH AND EDIT
      if (!(type == 'edtbl')) {
        el.append('<tr class="' + type + '" idx=' + idx + ' id=' + v.OWNER_CODE + '><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td style="min-width:100px" idx="ASSESSED_ACRES">$' + v.ASSESSED_ACRES + '</td><td idx="DATE_PAID">' + v.DATE_PAID + '</td><td style="min-width:120px" id="AMOUNT_PAID" idx="AMOUNT_PAID">$' + v.AMOUNT_PAID + '</td><td style="min-width:36px" idx="PAID">' + v.PAID + '</td><td class="more" id="more"><i id="morebtn" class="fa fa-list-alt" aria-hidden="true" data-toggle="tooltip" style="font-size: 22px"></i></td></tr>');
        // el.append('<tr class="' + type + '" idx=' + idx + ' id='+values.PIN+'><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td style="min-width:100px" idx="ASSESSED_ACRES">$' + v.ASSESSED_ACRES + '</td><td idx="DATE_PAID">' + values.DATE_PAID + '</td><td style="min-width:120px" id="AMOUNT_PAID" idx="AMOUNT_PAID">$'+ v.AMOUNT_PAID +'</td><td style="min-width:36px" idx="PAID">'+ v.PAID +'</td></tr>')
      }
    }

    if (type == 'edtbl') {
      el.append('<tr class="' + type + '" idx=' + idx + ' id=' + v.OWNER_CODE + '><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td idx="ASSESSED_ACRES">$' + v.ASSESSED_ACRES + '</td><td idx="DATE_PAID">' + v.DATE_PAID + '</td><td id="YEAR" idx="YEAR">' + v.YEAR + '</td><td style="min-width:100px" idx="PENALTY">' + v.PENALTY + '</td><td id="AMOUNT_PAID" idx="AMOUNT_PAID">$' + v.AMOUNT_PAID + '</td><td idx="PAID">' + v.PAID + '</td><td idx="EXCESS">' + v.EXCESS + '</td><td idx="ASSESSED_ACRES">' + v.ASSESSED_ACRES + '</td><td idx="TOT_BENEFIT">$' + v.TOT_BENEFIT + '</td></tr>')
      $('.moveUp').remove();
      $('.edtbl').append('<td class="moveUp" id="ZA"><i id="btnAdd" class="fa fa-arrow-circle-up btnAdd" aria-hidden="true" data-toggle="tooltip" style="font-size: 24px"></i></td>');
    }
  }

  var srw = $('#srchRslt').children().eq(1).children().eq(0).width();
  $('#srchHeader').children().eq(0).css('width', srw);
  var srw = $('#srchRslt').children().eq(1).children().eq(1).width();
  $('#srchHeader').children().eq(1).css('width', srw);
  var srw = $('#srchRslt').children().eq(1).children().eq(2).width();
  $('#srchHeader').children().eq(2).css('width', srw);
  var srw = $('#srchRslt').children().eq(1).children().eq(3).width();
  $('#srchHeader').children().eq(3).css('width', srw);
  var srw = $('#srchRslt').children().eq(1).children().eq(4).width();
  $('#srchHeader').children().eq(4).css('width', srw);
  var srw = $('#srchRslt').children().eq(1).children().eq(5).width();
  $('#srchHeader').children().eq(5).css('width', srw);
  var srw = $('#srchRslt').children().eq(1).children().eq(7).width();
  $('#srchHeader').children().eq(7).css('width', srw);

  $('.moveUp').click(function() {
    var el = $(this).siblings();
    $(this).parent().addClass('moveUp');
    $(this).siblings().removeClass('moveUp');
    var index = $(".edtbl").index($(this).parent());

    if ($(this).parent().attr('idx') == 'newRec') {
      bldSmryTbl(editList[index], index, 'newRec');
    } else {
      bldSmryTbl(editList[index], index);
    }

    if (index < 0) {
      var index = 0;
    }

    editList.splice(index, 1);
    $(this).parent().remove();
  });

  $('#DATE_PAID').one('click', function() {
    datepicker($(this))
  });

  $('#PAID').one('click', function() {
    dropDown($(this));
  });

}

function processEdits(changeList) {
  var addList = changeList.filter(function(val) {
    return val.newRecord
  });

  var updateList = changeList.filter(function(val) {
    return !(val.newRecord)
  })

  var status = getData.postEdits(updateList, addList);

  console.log('STATUS ', status)

var prm = status.promise();

prm.done(function(b){
  console.log("STATUS: ", b.status)

  if(b.status == "success"){
    editList = [];
    updateList = [];
    addList = [];
    $('.edtbl').remove();
  }else{
    alert('Post Edits Failed, check to make sure ArcMap or ArcCatalog are closed and try again');
  }

})




  // CLEAN DATA
  //globObj.editRecs.NewRec.OWNER = globObj.editRecs.NewRec.OWNER.replace('amp;','');
}