import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';

class ReadyGoView extends StatefulWidget {
  final Widget child;
  const ReadyGoView({Key? key, required this.child}) : super(key: key);

  @override
  State<ReadyGoView> createState() => _ReadyGoViewState();
}

class _ReadyGoViewState extends State<ReadyGoView> with SingleTickerProviderStateMixin {
  late final AnimationController _lottieController;
  bool finished = false;

  @override
  void initState() {
    super.initState();
    _lottieController = AnimationController(vsync: this);
    _lottieController.addStatusListener((status) {
      if (status == AnimationStatus.completed) {
        setState(() {
          finished = true;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: Alignment.topCenter,
      children: [
        AnimatedOpacity(
          opacity: finished ? 1 : 0.5,
          duration: const Duration(milliseconds: 300),
          child: widget.child,
        ),
        AnimatedOpacity(
          opacity: finished ? 0 : 1,
          duration: const Duration(milliseconds: 300),
          child: LottieBuilder.asset(
            'assets/lotties/ready.json',
            controller: _lottieController,
            repeat: false,
            onLoaded: (composition) {
              _lottieController
                ..duration = composition.duration
                ..forward();
            },
          ),
        ),
      ],
    );
  }
}
