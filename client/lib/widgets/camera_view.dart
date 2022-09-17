import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

class CameraView extends StatefulWidget {
  const CameraView({Key? key}) : super(key: key);

  @override
  State<CameraView> createState() => _CameraViewState();
}

class _CameraViewState extends State<CameraView> {
  late VideoPlayerController _controller;
  bool ready = false;

  @override
  void initState() {
    super.initState();
    _controller = VideoPlayerController.network(
      'http://192.168.1.102:4747/video',
    )..initialize().then((_) {
        setState(() {
          ready = true;
        });
        _controller.play();
      });
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15.0),
      ),
      elevation: 3,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(15.0),
        child: Builder(builder: (context) {
          if (!ready) {
            return Center(
              child: CircularProgressIndicator(
                color: Theme.of(context).primaryColor,
              ),
            );
          }
          return VideoPlayer(
            _controller,
          );
        }),
      ),
    );
  }

  @override
  void dispose() {
    super.dispose();
    _controller.dispose();
  }
}
