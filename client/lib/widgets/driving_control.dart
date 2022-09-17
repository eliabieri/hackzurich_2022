import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class DrivingControl extends StatefulWidget {
  const DrivingControl({Key? key}) : super(key: key);

  @override
  State<DrivingControl> createState() => _DrivingControlState();
}

class _DrivingControlState extends State<DrivingControl> {
  final FocusNode _focusNode = FocusNode();

  @override
  Widget build(BuildContext context) {
    FocusScope.of(context).requestFocus(_focusNode);
    return Column(
      children: [
        RotatedBox(
          quarterTurns: 3,
          child: DirectionButton(
            focusNode: _focusNode,
            keyboardKey: LogicalKeyboardKey.arrowUp,
          ),
        ),
        Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            RotatedBox(
              quarterTurns: 2,
              child: DirectionButton(
                focusNode: _focusNode,
                keyboardKey: LogicalKeyboardKey.arrowLeft,
              ),
            ),
            RotatedBox(
              quarterTurns: 1,
              child: DirectionButton(
                focusNode: _focusNode,
                keyboardKey: LogicalKeyboardKey.arrowDown,
              ),
            ),
            RotatedBox(
              quarterTurns: 0,
              child: DirectionButton(
                focusNode: _focusNode,
                keyboardKey: LogicalKeyboardKey.arrowRight,
              ),
            ),
          ],
        ),
      ],
    );
  }
}

class DirectionButton extends StatefulWidget {
  final LogicalKeyboardKey keyboardKey;
  final FocusNode focusNode;
  const DirectionButton({required this.focusNode, required this.keyboardKey, Key? key})
      : super(key: key);

  @override
  State<DirectionButton> createState() => _DirectionButtonState();
}

class _DirectionButtonState extends State<DirectionButton> {
  static const Color _defaultColor = Colors.grey;
  Color _color = _defaultColor;

  @override
  Widget build(BuildContext context) {
    return RawKeyboardListener(
      focusNode: widget.focusNode,
      onKey: (event) {
        if (event.isKeyPressed(widget.keyboardKey)) {
          setState(() {
            _color = Theme.of(context).primaryColor;
          });
        } else {
          setState(() {
            _color = _defaultColor;
          });
        }
      },
      child: Padding(
        padding: const EdgeInsets.all(4.0),
        child: FaIcon(
          FontAwesomeIcons.play,
          color: _color,
          size: 35,
        ),
      ),
    );
  }
}
