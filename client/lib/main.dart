import 'package:client/views/main_view.dart';
import 'package:client/views/ready_go_view.dart';
import 'package:flutter/material.dart';

void main() {
  runApp(const App());
}

class App extends StatelessWidget {
  const App({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Merkle Explorer',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
        fontFamily: 'ProximaNova',
        appBarTheme: const AppBarTheme(
          backgroundColor: Color(0xff13295d),
        ),
        primaryColor: const Color(0xff13295d),
      ),
      color: const Color(0xff13295d),
      home: const ReadyGoView(child: MainView()),
    );
  }
}
