<?php
/*
Plugin Name: Ultimate Member – Pending User Approvals
Description: Adds an admin page to view and approve pending Ultimate Member accounts.
Version: 1.0
Author: Burgh Tech
*/

if ( ! defined( 'ABSPATH' ) ) exit;

// Add menu page
add_action( 'admin_menu', function() {
    add_menu_page(
        'Pending Users',
        'Pending Users',
        'manage_options',
        'um-pending-users',
        'um_render_pending_users_page',
        'dashicons-groups',
        50
    );
});

// Render page
function um_render_pending_users_page() {
    if ( ! current_user_can( 'manage_options' ) ) return;

    // Approve user if clicked
    if ( isset($_GET['approve_user']) && is_numeric($_GET['approve_user']) ) {
        $user_id = intval($_GET['approve_user']);
        um_approve_user($user_id);
        echo '<div class="updated"><p>User ID ' . $user_id . ' approved.</p></div>';
    }

    // Get pending users
    $pending_users = get_users([
        'meta_key'   => 'account_status',
        'meta_value' => 'pending',
    ]);

    echo '<div class="wrap"><h1>Pending Users</h1>';

    if ( empty($pending_users) ) {
        echo '<p>No pending users 🎉</p>';
    } else {
        echo '<table class="widefat"><thead><tr>
                <th>ID</th><th>Name</th><th>Email</th><th>Actions</th>
              </tr></thead><tbody>';
        foreach ( $pending_users as $user ) {
            echo '<tr>
                    <td>' . $user->ID . '</td>
                    <td>' . esc_html($user->display_name) . '</td>
                    <td>' . esc_html($user->user_email) . '</td>
                    <td><a href="' . admin_url('admin.php?page=um-pending-users&approve_user=' . $user->ID) . '" class="button">Approve</a></td>
                  </tr>';
        }
        echo '</tbody></table>';
    }

    echo '</div>';
}

// Approve user function
function um_approve_user($user_id) {
    if ( function_exists('um_fetch_user') ) {
        um_fetch_user($user_id);
        UM()->user()->approve();
    }
}
