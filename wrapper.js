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

function jp_wrap(string, width, separator) {
	var segmenter = new TinySegmenter(); // インスタンス生成
	var segs = segmenter.segment(string); // 単語の配列が返る
	// console.log(segs.join(" | ")); // 表示
	var lines = [],
		line, len;
	while (segs.length > 0) {
		line = '';
		len = segs[0].length;
		width = Math.max(width, len);
		while (segs.length > 0 && line.length + len <= width) {
			line += segs.shift();
		}
		lines.push(line);
	}
	return lines.join(separator);
}
/*
$(function() {
	var width = 5;
	console.log("width: " + width);
	console.log(jp_wrap("TSを使った日本語の自動改行のテスト。", width, '\n'));
});
*/
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
		strs = $.map(strs, function(str, _) {
			var s = chunkString(str, width);
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