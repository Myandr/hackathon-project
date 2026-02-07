import 'dart:convert';
import 'package:http/http.dart' as http;

Future<void> sendWord(String word) async {
  final url = Uri.parse('http://127.0.0.1:8000/word');

  // JSON-Body
  final body = jsonEncode({'word': word});

  try {
    final response = await http.post(
      url,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: body,
    );

    if (response.statusCode == 200 || response.statusCode == 201) {
      // Antwort lesen (falls JSON)
      final data = jsonDecode(response.body);
      print('Antwort: $data.sentence');
    } else {
      print('Fehler: ${response.statusCode}');
      print('Response: ${response.body}');
    }
  } catch (e) {
    print('Ausnahme: $e');
  }
}
