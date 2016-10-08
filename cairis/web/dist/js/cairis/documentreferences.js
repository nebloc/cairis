/*  Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.

    Authors: Shamal Faily */


$("#documentReferencesClick").click(function(){
  createDocumentReferencesTable();
});

function createDocumentReferencesTable(){

  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/document_references",
    success: function (data) {
      window.activeTable = "DocumentReferences";
      setTableHeader();
      var theTable = $(".theTable");
      $(".theTable tr").not(function(){if ($(this).has('th').length){return true}}).remove();
      var textToInsert = [];
      var i = 0;

      $.each(data, function(key, item) {
        textToInsert[i++] = "<tr>";
        textToInsert[i++] = '<td><button class="editDocumentReferenceButton" value="' + key + '">' + 'Edit' + '</button> <button class="deleteDocumentReferenceButton" value="' + key + '">' + 'Delete' + '</button></td>';

        textToInsert[i++] = '<td name="theName">';
        textToInsert[i++] = key;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '<td name="theDocName">';
        textToInsert[i++] = item.theDocName;
        textToInsert[i++] = '</td>';

        textToInsert[i++] = '</tr>';
      });

      theTable.append(textToInsert.join(''));
      theTable.css("visibility","visible");
      activeElement("reqTable");
      sortTableByRow(0);
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  })
}

$(document).on('click', ".editDocumentReferenceButton", function () {
  var name = $(this).val();
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crossDomain: true,
    url: serverIP + "/api/document_references/name/" + name.replace(" ", "%20"),
    success: function (data) {
      fillOptionMenu("fastTemplates/editDocumentReferenceOptions.html", "#optionsContent", null, true, true, function () {
        $("#optionsHeaderGear").text("Document Reference properties");
        forceOpenOptions();
        var docNameSelect = $("#theDocName");
        var docName = data.theDocName;
        getDocNames(function(data) {
          $.each(data, function(key, obj) {
            docNameSelect.append($("<option></option>").attr("value",obj).text(obj));
          });
          docNameSelect.val(docName);
        });
        $.session.set("DocumentReference", JSON.stringify(data));
        $('#editDocumentReferenceOptionsForm').loadJSON(data, null);
      });
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText + ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
});

optionsContent.on('click', '#UpdateDocumentReference', function (e) {
  e.preventDefault();
  var dr = JSON.parse($.session.get("DocumentReference"));
  var oldName = dr.theName;
  dr.theName = $("#theName").val();
  dr.theDocName = $("#theDocName").val();
  dr.theContributor = $("#theContributor").val();
  dr.theExcerpt = $("#theExcerpt").val();

  if($("#editDocumentReferenceOptionsForm").hasClass("new")){
    postDocumentReference(dr, function () {
      createDocumentReferencesTable();
      $("#editDocumentReferenceOptionsForm").removeClass("new")
    });
  }
  else {
    putDocumentReference(dr, oldName, function () {
      createDocumentReferencesTable();
    });
  }
});

$(document).on('click', '.deleteDocumentReferenceButton', function (e) {
  e.preventDefault();
  deleteDocumentReference($(this).val(), function () {
    createDocumentReferencesTable();
  });
});

$(document).on("click", "#addNewDocumentReference", function () {
  fillOptionMenu("fastTemplates/editDocumentReferenceOptions.html", "#optionsContent", null, true, true, function () {
    $("#editDocumentReferenceOptionsForm").addClass("new");
    $.session.set("DocumentReference", JSON.stringify(jQuery.extend(true, {},documentReferenceDefault )));
    $("#optionsHeaderGear").text("Document Reference properties");
    forceOpenOptions();
    var docNameSelect = $("#theDocName");
    getDocNames(function(data) {
      $.each(data, function(key, obj) {
        docNameSelect.append($("<option></option>").attr("value",obj).text(obj));
      });
    });
  });
});


function putDocumentReference(dr, oldName, usePopup, callback){
  var output = {};
  output.object = dr;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);
  debugLogger(output);

  $.ajax({
    type: "PUT",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/document_references/name/" + oldName.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      if(usePopup) {
        showPopup(true);
      }
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      if(usePopup) {
        var error = JSON.parse(xhr.responseText);
        showPopup(false, String(error.message));
      }
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function postDocumentReference(dr, callback){
  var output = {};
  output.object = dr;
  output.session_id = $.session.get('sessionID');
  output = JSON.stringify(output);
  debugLogger(output);

  $.ajax({
    type: "POST",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    data: output,
    url: serverIP + "/api/document_references" + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function deleteDocumentReference(name, callback){
  $.ajax({
    type: "DELETE",
    dataType: "json",
    contentType: "application/json",
    accept: "application/json",
    crossDomain: true,
    processData: false,
    origin: serverIP,
    url: serverIP + "/api/document_references/name/" + name.replace(" ","%20") + "?session_id=" + $.session.get('sessionID'),
    success: function (data) {
      showPopup(true);
      if(jQuery.isFunction(callback)){
        callback();
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      var error = JSON.parse(xhr.responseText);
      showPopup(false, String(error.message));
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}

function getDocNames(callback){
  $.ajax({
    type: "GET",
    dataType: "json",
    accept: "application/json",
    data: {
      session_id: String($.session.get('sessionID'))
    },
    crfossDomain: true,
    url: serverIP + "/api/dimensions/table/external_document",
    success: function (data) {
      if(jQuery.isFunction(callback)){
        callback(data);
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      debugLogger(String(this.url));
      debugLogger("error: " + xhr.responseText +  ", textstatus: " + textStatus + ", thrown: " + errorThrown);
    }
  });
}