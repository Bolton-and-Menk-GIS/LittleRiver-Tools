// BUILD TABLE
$(function() {
	var inp;

$('#search').keypress(function(evt){
  evt.stopPropagation();
          if(evt.which == 13){
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
if($('#summary').children().children().hasClass('newRec')){
	console.log("HIHIH");
    // var id = $('.smryTbl').attr('id');
    var dataAttr = getData.getData().data;
    var rec = null;
	// var recs = getEditRecords(rec);
	var recs = getData.getEdits(rec);
		// EDIT BY CALEB
		if ('NewRec' in recs.edits){
			if (!recs.edits.NewRec.PARCEL_ID){
				alert('You must enter a valid Parcel ID for record!');
				return
			}else {
				recs.edits.NewRec.PIN = recs.edits.NewRec.PARCEL_ID.replace(/[-.]/g, "")
			}
		}
	    globObj.editRecs = recs;
	    buildEditTbl(recs.edits, 'newRec');

          // :::: EFFECTS :::: 
	    $('.newRec').remove();
      // $('.newRec').fadeOut();
    // :::: EFFECTS :::: 
}else{
	// EXISTING RECORD (EDIT)
    var id = $('.smryTbl').attr('idx');
    // var recs = getEditRecords(globObj.attributes[id]);
    var dataAttr = getData.getData().data
    console.log("DATA ATTR?", dataAttr.attributes[id], "ID?????????????", id);
    var recs = getData.getEdits(dataAttr.attributes[id]);
    console.log('RECS??', recs)
        globObj.editRecs = recs;
        console.log("ID? ", id)
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
    console.log('HUH?')

        // :::: EFFECTS :::: 
  $('.smryTbl').remove();
  $('.newRec').remove();
  //   $('.smryTbl').fadeOut();
  // $('.newRec').fadeOut();
    // :::: EFFECTS :::: 

    $('#summary').children().append('<tr class="newRec" id="newRec"><td class="nr" idx="OWNER"></td><td class="nr" idx="OWNER_CODE"></td><td class="nr" idx="PARCEL_ID"></td><td class="nr" idx="ASSESSED_ACRES"></td><td class="nr" idx="DATE_PAID" id="DATE_PAID"></td><td class="nr" idx="PENALTY"></td><td class="nr" idx="AMOUNT_PAID"></td><td class="nr" id="PAID" idx="PAID"></td><td class="nr" idx="EXCESS"></td></tr>');

// $('.smryTbl').append('<td class="moveDown" id="ZA"><i id="moveDown" class="fa fa-arrow-circle-down" aria-hidden="true" data-toggle="tooltip" style="font-size: 24px"></i></td>')

//<td idx="OWNER"><input type="text" class="newRec" id="input0"></td>

// DATE STUFF

$('#DATE_PAID').one('click', function(){
  datepicker($(this));
})

    $('#PAID').one('click', function(){
  console.log("PAID CLICKED");
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
      var rw = $('<input type="text" tabindex="1" class="newRec" id="input0" placeholder="Add New Record" value="' + fm + '" style="width: 250px">');
      var cw = $('input[name="hiddenField"]');
      $(this).inlineEdit(rw, cw);
      displayBtn();
    });
  });

  $('#postEdits').click(function(){
  	processEdits(editList);
  });
});

function datepicker(el){
  el.empty();
  el.append('<input type="text" class="inpt" id="dp" style="width: 70px; height: 20px; padding: 3px; padding-bottom: 0px; padding-top:0px">')
  $('#dp').datepicker({dateFormat: "m/dd/yy"});
}

function dropDown(el){
  console.log("??")
    el.empty();
    el.append('<div><select id="soflow"><option select>Y</option><option>N</option></select></div>');
}


$.fn.inlineEdit = function(RW, CW) {
  $(this).click(function() {
        console.log("WHAT IS THIS???? ", $(this))
    if(this.id == 'DATE_PAID' || this.id == 'PAID' || this.id=='mvdn'){
    }
    else {

    var el = $(this);

    el.siblings().removeClass('smryData');
    el.hide();
    el.after(RW);
    RW.focus();

    console.log('LOOK FOR $$$', el.html().indexOf('$') < 0)
    RW.blur(function() {
      console.log('CW VAL', this, 'AND CW', $(this).parent(), 'HTML ', $(this).html())
      if ($(this).val() != "") {
        CW.val($(this).val()).change();
        el.text($(this).val());
      }

      // :::: EFFECTS ::::
      $(this).remove();

      // :::: EFFECTS ::::

      console.log('ELAFTER', el.after());
      el.after().addClass('smryData');
      el.siblings().removeClass('smryData');

      el.show();
    });
    }
//if (!($(this).parent().hasClass('newRec')))

    // else{
    //   console.log("???SDLFH")
    //   var stuff = $(this).html();
    //    $(this).text($(this).val());
    //    $(this).addClass('smryData')
    // }
  });

}

  var editList = [];

function buildEditTbl(recs, idx) {
  var rec = recs.NewRec
    // $('#editList').append('<tr class="edtbl" id='+idx+'><td id="OWNER">'+rec.OWNER+'</td><td id="PARCEL_ID">'+rec.PARCEL_ID+'</td><td id="amountPaid">'+rec.amountPaid+'</td><td id="date">'+rec.date+'</td><td id="PENALTY"></td><td id="TOT_ADMIN_FEE"></td><td id="PAID"></td><td id="EXCESS"></td></tr>');
  console.log("WHAT ARE THE RECS?? ", recs)
  buildTable($('#editList'), 'edtbl', rec, idx);
    // $('#editView').css('display', 'table');

    $('#editView').slideDown();

  editList.push(rec);
  console.log("THE EDIT LIST: ", editList);
}

function bldSummaryBox(code){
  var info = getData.getOwnerInfo(code);

  var uri = 'http://localhost:5001/rest/getOwnerSummary?code=' + code;
  var info = LocalUtils.getJson(uri, 'jsonp', 'POST').done(function(res){
    
    // format Data
    var TadminFee = LocalUtils.toFixed(res.total_admin_fee);
    var totalBill = LocalUtils.toFixed(res.total_bill);
    var assmnt = LocalUtils.toFixed(res.total_assessment);

    // BUILD LB TABLE
    $('.tblData').empty();
    $('#AF').children().children().find('td').remove();
    $('#ownerData').append(res.code);
    $('#nameData').append(res.name);
    $('#dpData').append('7/7/2016');
    $('#adminFeeData').append('$'+TadminFee);
    $('#billData').append('$'+totalBill);
    $('#assessData').append('$'+assmnt);
    $('#penData').append('$'+res.penalty);
  res.assessments.map(function(va){
    var adminFee = LocalUtils.toFixed(va.admin_fee);  

  $('#AF').append('<tr><td class="tblData" style="padding-left: 10px">'+va.pin+'</td><td class="tblData" style="padding-left: 10px">$'+adminFee+'</td></tr>');
})

  });

  LightBox($('<div id="lb-content"></div>'));
  $('#lb-content').append($('#summaryView'));
  $('#lb-content').show();
  $('#summaryView').css('display','block');
}

function bldSmryTbl(rec, idx, newRecord) {
  // $('#summaryView').css('display', 'table');

    // $('#summaryView').slideDown();

  if (!rec) {
    console.log("RAR")
  }
  $('.smryTbl').remove();
if (newRecord){
	console.log("NEW RECORD HEREE????")
	  buildTable($('#summary'), 'smryTbl', rec, idx, newRecord);
}
else{
	console.log("&&&&EW RECORD HEREE????")
  // $('#summary').append('<tr class="smryTbl" id='+idx+'><td id="OWNER">'+rec.OWNER+'</td><td id="PARCEL_ID">'+rec.PARCEL_ID+'</td><td id="amountPaid">$'+rec.amountPaid+'</td><td id="date">'+rec.date+'</td><td id="PENALTY">a</td><td id="TOT_ADMIN_FEE"></td><td id="PAID"></td><td id="EXCESS"></td></tr>');
  buildTable($('#summary'), 'smryTbl', rec, idx);
 }

  $('.smryTbl').children().one("click", function(event) {


    $(this).siblings().removeClass('smryData');
    $(this).addClass('smryData');

    console.log("BEFORE ", $(this).before());

    console.log("THIS ", this, 'whats a', $(this).html());
    var fm = $(this).html();
    var rw = $('<input type="text" class="inpt" id="input' + idx + '" value="' + fm + '" style="width: 250px">');
    var cw = $('input[name="hiddenField"]');
    $(this).inlineEdit(rw, cw);
    //<input type="text" id="row-1-age" name="row-1-age" value="61">
  });
displayBtn();
  //OWNER_CODE
}


function displayBtn(){
    if ($('#summary').children().children().find('td').length > 0){
    $('#stageEdits').css('display', 'inline');
    $('#btnContainer').css('width', '65px');
  }else{
    $('#stageEdits').css('display', 'none');
    $('#btnContainer').css('width', '28px');
  }
}

function bldSrchTbl(res) {
  res.forEach(function(v, idx) {
    buildTable($('#srchRslt'), 'srchTbl', v, idx);
    // $('#srchRslt').append('<tr class="srchTbl" id='+idx+'><td id="OWNER">'+v.OWNER+'</td><td id="PARCEL_ID">'+v.PARCEL_ID+'</td><td id="amountPaid">$'+v.amountPaid+'</td><td id="date">'+v.date+'</td></tr>');
  });

$('.more').click(function(evt){
  console.log("CLICKED MORE BUTTON!!")
  evt.stopPropagation();
  console.log("WHAT IS THIS PARENT?", $(this).parent()[0]);
  var gid = $(this).parent()[0].id
  console.log('GID', $(this).parent()[0].id)
  bldSummaryBox(gid)
})

  // $('.srchTbl').click(function(){
  $('.srchTbl').click(function(a) {
  $('.newRec').remove()
  var idx = $(this).attr('idx');
    console.log("THIS?", this, 'a', a)
    console.log("SUMMARY TABLE STUFF:: ", res[idx], idx)
    bldSmryTbl(res[idx], idx);
  });
}

var counter = (function() {
  var _privateCounter = 0;
  function changeBy(val) {
    _privateCounter += val;
  }
  function reset(){
  	_privateCounter = 0;
  }
  return {
    increment: function(val) {
      changeBy(val);
    },
    decrement: function() {
      changeBy(-1);
    },
    reset: function(){
    	reset();
    },
    value: function() {
      return _privateCounter;
    }
  };   
})();

function buildTable(el, type, v, idx, newRecord) {
  console.log('vals', v);

  // counter.increment(1);
  if (type == 'smryTbl') {
  	$('.newRec').remove();
    if(newRecord){
    	console.log('V IS? ',v)
    el.append('<tr class="' + type + ' newRec" idx=' + idx + ' id='+v.OWNER_CODE+'><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td  idx="ASSESSED_ACRES">' + v.ASSESSED_ACRES + '</td><td id="DATE_PAID" idx="DATE_PAID">' + v.DATE_PAID + '</td><td idx="PENALTY">'+ v.PENALTY+'</td><td id="AMOUNT_PAID" idx="AMOUNT_PAID">'+ v.AMOUNT_PAID +'</td><td id="PAID" idx="PAID">'+ v.PAID +'</td><td idx="EXCESS">'+ v.EXCESS +'</td></tr>');
    }else{
    	 el.append('<tr class="' + type + '" idx=' + idx + ' id='+v.OWNER_CODE+'><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td idx="ASSESSED_ACRES">' + v.ASSESSED_ACRES + '</td><td id="DATE_PAID" idx="DATE_PAID">' + v.DATE_PAID + '</td><td idx="PENALTY">'+ v.PENALTY+'</td><td id="AMOUNT_PAID" idx="AMOUNT_PAID">'+ v.AMOUNT_PAID +'</td><td id="PAID" idx="PAID">'+ v.PAID +'</td><td idx="EXCESS">'+ v.EXCESS +'</td></tr>');
    }
   // $('.smryTbl').append('<td class="moveDown" id="mvdn"><i id="stageEdits" class="fa fa-arrow-circle-down" aria-hidden="true" data-toggle="tooltip" style="font-size: 24px"></i></td>')

  } else {
  	console.log("VAL PIN?? ", v)
  	if(!(v.PIN)){
  		 counter.increment(1);
  		el.append('<tr class="' + type + '" idx=' + idx + ' id=nr'+counter.value()+'><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td idx="ASSESSED_ACRES">' + v.ASSESSED_ACRES + '</td><td idx="DATE_PAID">' + v.DATE_PAID + '</td><td idx="PENALTY">'+ v.PENALTY+'</td><td id="AMOUNT_PAID" idx="AMOUNT_PAID">'+ v.AMOUNT_PAID +'</td><td idx="PAID">'+ v.PAID +'</td></tr>')
  	}else{
      var values = {};

      Object.keys(v).forEach(function(key){
        values[key] = v[key];
        if (v[key] == null){
                            console.log('V v', v[key])
          // values[key] = 'No Value';
          // v[key] = 'No Value'
          // values[key] = 'No Value';

        }
    })
      // THIS TABLE DEFINITION REPRESENTS SEARCH AND EDIT
     if (!(type == 'edtbl')){
        el.append('<tr class="' + type + '" idx=' + idx + ' id='+v.OWNER_CODE+'><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td style="min-width:100px" idx="ASSESSED_ACRES">$' + v.ASSESSED_ACRES + '</td><td idx="DATE_PAID">' + v.DATE_PAID + '</td><td style="min-width:120px" id="AMOUNT_PAID" idx="AMOUNT_PAID">$'+ v.AMOUNT_PAID +'</td><td style="min-width:36px" idx="PAID">'+ v.PAID +'</td><td class="more" id="more"><i id="morebtn" class="fa fa-list-alt" aria-hidden="true" data-toggle="tooltip" style="font-size: 22px"></i></td></tr>');
  		// el.append('<tr class="' + type + '" idx=' + idx + ' id='+values.PIN+'><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td style="min-width:100px" idx="ASSESSED_ACRES">$' + v.ASSESSED_ACRES + '</td><td idx="DATE_PAID">' + values.DATE_PAID + '</td><td style="min-width:120px" id="AMOUNT_PAID" idx="AMOUNT_PAID">$'+ v.AMOUNT_PAID +'</td><td style="min-width:36px" idx="PAID">'+ v.PAID +'</td></tr>')
  }
  	}
    
    if (type == 'edtbl') {
            el.append('<tr class="' + type + '" idx=' + idx + ' id='+v.OWNER_CODE+'><td idx="OWNER">' + v.OWNER + '</td><td idx="OWNER_CODE">' + v.OWNER_CODE + '</td><td idx="PARCEL_ID">' + v.PARCEL_ID + '</td><td idx="ASSESSED_ACRES">$' + v.ASSESSED_ACRES + '</td><td idx="DATE_PAID">' + v.DATE_PAID + '</td><td style="min-width:100px" idx="PENALTY">'+ v.PENALTY+'</td><td id="AMOUNT_PAID" idx="AMOUNT_PAID">$'+ v.AMOUNT_PAID +'</td><td idx="PAID">'+ v.PAID +'</td><td idx="EXCESS">'+ v.EXCESS +'</td></tr>')
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

    $('.moveUp').click(function(){
		var el = $(this).siblings();
		$(this).parent().addClass('moveUp');
		$(this).siblings().removeClass('moveUp');
  	console.log('CLICKED!', $(el))
  	console.log('PARENT: ', $(this).parent().attr('idx'));

    var index = $( ".edtbl" ).index($(this).parent());
    console.log("INDEX?>?", index, "WHATUPPP?? ", $(this));

if ($(this).parent().attr('idx') == 'newRec'){
	console.log('BUILDSMRYTBL: ', this)
	  bldSmryTbl(editList[index], index, 'newRec');
	}else{
			console.log('THIS TOO!??')
  bldSmryTbl(editList[index], index);
	}
	console.log("EDIT LIST?? ", editList, "INDEX ?", index+1)

	if(index < 0){
		var index = 0;
	}

	editList.splice(index, 1);
$(this).parent().remove();
  });

    $('#DATE_PAID').one('click', function(){
  console.log('WHAT THE?????????')
  datepicker($(this))
});

  $('#PAID').one('click', function(){
  console.log("PAID CLICKED");
  dropDown($(this));
});

}

function processEdits(changeList) {
	console.log('POST EDITS!', changeList);
	var addList = changeList.filter(function(val){
		console.log("VAL?? ", val);
		console.log("VAL NR: ", val.newRecord)
		return val.newRecord
	});

console.log('FILTERED', addList)

	var updateList = changeList.filter(function(val){
		return !(val.newRecord)
	})

getData.postEdits(updateList, addList);

	console.log('UPDATES', updateList, 'ADDS', addList);

  editList = [];
	updateList = [];
  addList = [];
	$('.edtbl').remove();


  // CLEAN DATA
  //globObj.editRecs.NewRec.OWNER = globObj.editRecs.NewRec.OWNER.replace('amp;','');
}