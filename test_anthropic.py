#!/usr/bin/env python3
"""
Quick test script to verify Anthropic SDK installation and API connectivity.
"""

import anthropic
import sys

def test_anthropic_setup():
    """Test basic Anthropic SDK functionality."""

    print("=" * 60)
    print("ANTHROPIC SDK TEST")
    print("=" * 60)
    print()

    # Check SDK version
    print(f"[OK] SDK Version: {anthropic.__version__}")
    print()

    # Initialize client
    try:
        client = anthropic.Anthropic()
        print("[OK] Client initialized successfully")
        print()
    except Exception as e:
        print(f"[FAIL] Failed to initialize client: {e}")
        sys.exit(1)

    # Make a simple API call
    print("Testing API connectivity...")
    print("Sending a simple message to Claude...")
    print()

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": "Say 'Hello! API is working!' and nothing else."
                }
            ]
        )

        print("[OK] API call successful!")
        print()
        print("-" * 60)
        print("Response from Claude:")
        print("-" * 60)
        print(message.content[0].text)
        print("-" * 60)
        print()

        print("=" * 60)
        print("SUCCESS - ALL TESTS PASSED!")
        print("=" * 60)
        print()
        print("Your Anthropic SDK is fully functional and ready to use.")

    except anthropic.AuthenticationError:
        print("[FAIL] Authentication failed!")
        print("  Check that your ANTHROPIC_API_KEY is set correctly.")
        sys.exit(1)
    except anthropic.APIError as e:
        print(f"[FAIL] API Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_anthropic_setup()
