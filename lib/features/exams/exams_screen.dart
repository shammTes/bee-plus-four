import 'package:flutter/material.dart';

class ExamsScreen extends StatelessWidget {
  const ExamsScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return ListView(padding: const EdgeInsets.all(16), children: [
      Text('Exams', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold)),
      const SizedBox(height: 8),
      const Text('Matriculation & model exams expand via JSON packs.'),
      const SizedBox(height: 16),
      const Card(child: ListTile(leading: Icon(Icons.assignment), title: Text('Matriculation'), subtitle: Text('Offline catalogue'))),
      const Card(child: ListTile(leading: Icon(Icons.description), title: Text('Model exams'), subtitle: Text('Year index'))),
    ]);
  }
}
