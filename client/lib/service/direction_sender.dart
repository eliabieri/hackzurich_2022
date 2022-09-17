import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

enum Direction {
  up,
  down,
  left,
  right,
}

class DirectionSender {
  static void send(Direction direction) {
    final url = Uri.http('127.0.0.1:8000', 'drive/${describeEnum(direction)}');
    try {
      http.get(url);
    } catch (e) {
      debugPrint("Could not update drive direction");
    }
  }
}
