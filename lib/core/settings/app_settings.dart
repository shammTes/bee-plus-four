import 'package:flutter/material.dart';
import 'package:hive_flutter/hive_flutter.dart';

import '../l10n/app_strings.dart';

/// Language + theme preferences (offline).
class AppSettings extends ChangeNotifier {
  AppSettings._();
  static final instance = AppSettings._();

  static const _boxName = 'settings';
  Box? _box;

  bool darkMode = false;
  bool tigrinya = false;

  Future<void> init() async {
    _box = await Hive.openBox(_boxName);
    darkMode = (_box?.get('dark') as bool?) ?? false;
    tigrinya = (_box?.get('ti') as bool?) ?? false;
    AppStrings.tigrinya = tigrinya;
  }

  Future<void> setDark(bool v) async {
    darkMode = v;
    await _box?.put('dark', v);
    notifyListeners();
  }

  Future<void> setTigrinya(bool v) async {
    tigrinya = v;
    AppStrings.tigrinya = v;
    await _box?.put('ti', v);
    notifyListeners();
  }
}
