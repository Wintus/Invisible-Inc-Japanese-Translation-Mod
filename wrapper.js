'use strict'

$(function() {
	var min = 8,
		max = 50;
	var options = $.map(Array(max - min + 1), function(_, i) {
		i += min;
		return "<option value=" + i + ">" + i + "</option>";
	}).join('\n');
	$('#width').html(options);
	$('#width').val(min * 2);
});

function chunkJp(string, width) {
	var segmenter = new TinySegmenter(); // インスタンス生成
	var segs = segmenter.segment(string); // 単語の配列が返る
	var lines = [],
		line, len;
	while (segs.length > 0) {
		line = '';
		while (segs.length > 0 && line.length + segs[0].length <= width) {
			width = Math.max(width, segs[0].length); // avoid infinit loop
			line += segs.shift();
		}
		lines.push(line);
	}
	return lines;
}

function wrapJp(string, width, separator) {
	return chunkJp(string, width).join(separator);
}

function splitBy(string, separator) {
	return string.split(separator);
}

function chunkString(string, length) {
	if (string === '') return string;
	return string.match(new RegExp("(.{1," + length + "})", 'g'));
}

function insertSpaces(string, length) {
	return chunkString(string, length).join(' ');
}

function joinBy(string, separator) {
	if (string === '') return string;
	return string.join(separator);
}

$(function() {
	$('#btn').click(function() {
		var input = $('#input').val();
		var strs = input.split("\\n");
		var width = parseInt($('#width').val());

		var jp = $('input[name=jp_wrap]:checked').val() === '1';
		var wrap = jp ? chunkJp : chunkString;

		strs = $.map(strs, function(str, _) {
			var s = wrap(str, width);
			return Array(s);
		});
		var result = $.map(strs, function(str, _) {
			return joinBy(str, ' ');
		}).join('\\n');
		$('#output').text(result);

		var br = "<br>";
		$('#result').html(
			joinBy(
				$.map(strs, function(str, _) {
					return joinBy(str, br);
				}), br));
	});
	$('#btn').click();
});