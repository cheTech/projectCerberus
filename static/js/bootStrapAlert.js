bootstrap_alert = function() {}
bootstrap_alert.warning = function(message) {
	$('#alert-modal').html('<div class="modal-dialog" role="document"> <div class="modal-content"> <div class="modal-header">  <button type="button" class="close" data-dismiss="modal" aria-label="Закрыть"> <span aria-hidden="true">&times;</span> </button> </div> <div class="modal-body">' + message + ' </div> <div class="modal-footer"> <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button> </div> </div> </div>');
	$('#alert-modal').modal('show');
}