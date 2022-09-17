import 'package:client/widgets/camera_view.dart';
import 'package:client/widgets/office_map.dart';
import 'package:flutter/material.dart';

import '../widgets/driving_control.dart';

class MainView extends StatelessWidget {
  const MainView({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        leadingWidth: 150,
        leading: Container(
          margin: const EdgeInsets.only(left: 15),
          child: Image.asset(
            'assets/imgs/merkle_logo.png',
          ),
        ),
        title: const Text("Explorer"),
      ),
      body: Container(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Expanded(
              child: Stack(
                children: const [
                  CameraView(),
                  Positioned(
                    right: 15,
                    bottom: 15,
                    child: DrivingControl(),
                  ),
                ],
              ),
            ),
            const SizedBox(
              height: 15,
            ),
            const OfficeMap(),
          ],
        ),
      ),
    );
  }
}
