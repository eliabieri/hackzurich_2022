import 'package:flutter/material.dart';

class OfficeMap extends StatelessWidget {
  const OfficeMap({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15.0),
      ),
      elevation: 3,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(15.0),
        child: Image.asset('assets/imgs/grundriss.png'),
      ),
    );
  }
}
