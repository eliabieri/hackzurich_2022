import 'package:flutter/material.dart';
import 'package:flutter_vlc_player/flutter_vlc_player.dart';

class CameraView extends StatefulWidget {
  const CameraView({Key? key}) : super(key: key);

  @override
  State<CameraView> createState() => _CameraViewState();
}

class _CameraViewState extends State<CameraView> {
  late VlcPlayerController _videoPlayerController;
  bool ready = false;

  @override
  void initState() {
    super.initState();

    _videoPlayerController = VlcPlayerController.network(
      'http://192.168.1.101:8080/video',
      hwAcc: HwAcc.full,
      options: VlcPlayerOptions(
          video: VlcVideoOptions([
        VlcVideoOptions.dropLateFrames(true),
        VlcVideoOptions.skipFrames(true),
        VlcAdvancedOptions.liveCaching(0),
        VlcAdvancedOptions.networkCaching(0)
      ])),
    );
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
        child: VlcPlayer(
          controller: _videoPlayerController,
          aspectRatio: 4 / 3,
          placeholder: const Center(child: CircularProgressIndicator()),
        ),
      ),
    );
  }
}
