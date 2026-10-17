<?php
/**
 * Ryedale Removals — form handler for the quote and contact forms.
 *
 * Works on any standard PHP host (cPanel, Plesk, 20i, Krystal, IONOS etc.).
 * 1. Set $TO to the inbox that should receive enquiries.
 * 2. Set $FROM to an address on your own domain (helps deliverability).
 * Not on PHP hosting? See README.md for the Formspree / Netlify Forms option.
 */

$TO   = 'hello@ryedaleremovals.co.uk';
$FROM = 'website@ryedaleremovals.co.uk';
$SITE = 'Ryedale Removals';

$wantsJson = isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false;

function finish($ok, $wantsJson) {
    if ($wantsJson) {
        http_response_code($ok ? 200 : 400);
        header('Content-Type: application/json');
        echo json_encode(['ok' => $ok]);
    } else {
        header('Location: ' . ($ok ? 'thank-you.html' : 'contact.html?error=1'));
    }
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') finish(false, $wantsJson);

// Honeypot: real visitors never fill this hidden field
if (!empty($_POST['website'])) finish(true, $wantsJson);

$clean = function ($v) {
    if (is_array($v)) $v = implode(', ', $v);
    $v = trim(strip_tags((string) $v));
    return str_replace(["\r", "\n"], ' ', mb_substr($v, 0, 5000));
};

$name  = $clean($_POST['name'] ?? '');
$email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
$form  = $clean($_POST['form'] ?? 'Enquiry');

if ($name === '' || !$email) finish(false, $wantsJson);

$lines = [];
foreach ($_POST as $key => $value) {
    if (in_array($key, ['website', 'form'], true)) continue;
    $label = ucwords(str_replace(['_', '[]'], [' ', ''], $key));
    $text  = is_array($value) ? implode(', ', array_map('strip_tags', $value)) : trim(strip_tags((string) $value));
    if ($text !== '') $lines[] = $label . ': ' . $text;
}

$subject = "$SITE — new $form from $name";
$body    = "New $form received from the website\n\n" . implode("\n", $lines) . "\n\nSent: " . date('D j M Y H:i');
$headers = [
    'From: ' . $SITE . ' <' . $FROM . '>',
    'Reply-To: ' . $name . ' <' . $email . '>',
    'Content-Type: text/plain; charset=UTF-8',
];

$ok = mail($TO, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, implode("\r\n", $headers));
finish($ok, $wantsJson);
