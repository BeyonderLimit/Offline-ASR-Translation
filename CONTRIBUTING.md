# Contributing to Real-Time Speech Translation

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your system information (OS, Python version, etc.)
- Any relevant error messages or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue with:
- A clear description of the enhancement
- Why this enhancement would be useful
- Any implementation ideas you might have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clear, commented code
   - Follow the existing code style
   - Add tests if applicable

3. **Test your changes**
   - Ensure the application still runs
   - Test with different inputs
   - Check for any new warnings or errors

4. **Commit your changes**
   ```bash
   git commit -m "Add feature: description of your changes"
   ```
   - Use clear, descriptive commit messages
   - Reference any related issues

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots/videos if relevant

## Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/BeyonderLimit/Offline-ASR-Translation.git
   cd realtime-speech-translation
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download required models (see README.md)

## Code Style

- Use **4 spaces** for indentation (no tabs)
- Follow **PEP 8** guidelines
- Use descriptive variable names
- Add comments for complex logic
- Keep functions focused and single-purpose

## Testing

Before submitting a PR:
- [ ] Test with English → Spanish translation
- [ ] Verify audio input works correctly
- [ ] Verify audio output works correctly
- [ ] Check that logging suppression works
- [ ] Test on your target platform (Linux/Mac/Windows)

## Areas for Contribution

We especially welcome contributions in:

- **Additional language pairs** - Adding support for more languages
- **Performance improvements** - Optimizing translation/audio processing
- **UI/UX** - Creating a GUI interface
- **Documentation** - Improving docs, adding examples
- **Testing** - Adding unit tests and integration tests
- **Error handling** - Improving error messages and recovery
- **Platform support** - Better cross-platform compatibility

## Questions?

Feel free to open an issue with the label `question` if you need clarification on anything.

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what is best for the community
- Show empathy towards others

Thank you for contributing! 🎉
